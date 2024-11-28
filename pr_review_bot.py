import openai
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.devops.v5_0.git.models import GitPullRequestSearchCriteria,Comment, CommentThread, CommentThreadStatus

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Azure DevOps Organization and Project details from environment variables
organization_url = os.getenv("AZURE_ORG_URL")
personal_access_token = os.getenv("AZURE_PAT")
project_name = os.getenv("PROJECT_NAME")
repository_id = os.getenv("REPO_ID")
max_tokens = os.getenv("MAX_TOKENS")
model_version = os.getenv("MODEL_VERSION")

# List of authors to ignore
IGNORED_AUTHORS = os.getenv("IGNORED_AUTHORS", "").split(",")

# Authenticate to Azure DevOps
def get_azure_devops_connection():
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    return connection

# Get pull requests from Azure DevOps
def get_pull_requests():
    connection = get_azure_devops_connection()
    criteria = GitPullRequestSearchCriteria(status='active')
    
    git_client = connection.clients.get_git_client()
    pull_requests = git_client.get_pull_requests(
        project=project_name,
        repository_id=repository_id,
        search_criteria=criteria

    )
    return pull_requests

# Check if PR author is ignored
def is_author_ignored(author):
    return author.lower() in [ignored_author.lower() for ignored_author in IGNORED_AUTHORS]

# Filter PRs created in the last 24 hours
def is_recent_pr(creation_date):
    now = datetime.utcnow()
    pr_date = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%SZ")  # Azure DevOps uses ISO 8601 format
    return now - pr_date <= timedelta(days=1)

# Analyze the PR diff using OpenAI
def analyze_pr_diff(pr_id, diff):
    prompt = f"Review the following pull request provide feedback to all modified files give attention to time complexity and clean code principles:\n{diff}"
    response = openai.Completion.create(
        model=model_version, 
        prompt=prompt, 
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()

# Comment on the pull request
def comment_on_pr(pr_id, comment):
    connection = get_azure_devops_connection()
    git_client = connection.clients.get_git_client()

    # Create a comment thread
    thread = CommentThread(
        comments=[Comment(content=comment)],
        status=CommentThreadStatus.active
    )

    # Add the comment thread to the pull request
    git_client.create_thread(
        repository_id=repository_id,
        project=project_name,
        pull_request_id=pr_id,
        thread=thread
    )
    print(f"Comment posted on PR #{pr_id}")

# Fetch the diff content of a pull request
def fetch_pr_diff(pr_id):
    connection = get_azure_devops_connection()
    git_client = connection.clients.get_git_client()
    
    # Fetch the pull request changes
    changes = git_client.get_pull_request_changes(
        repository_id=repository_id,
        project=project_name,
        pull_request_id=pr_id
    )
    
    # Combine all file diffs into a single string
    diff_content = ""
    for change in changes.changes:
        if change.item.is_folder:  # Skip folder-level changes
            continue
        diff_content += f"File: {change.item.path}\n"
        diff_content += f"Change Type: {change.change_type}\n"
        if change.change_type == "edit" and hasattr(change, "diffs"):
            diff_content += f"Diff:\n{change.diffs}\n"  # Adjust as per API response
    
    return diff_content

# Main function to fetch PRs and review them
def review_pull_requests():
    pull_requests = get_pull_requests()
    for pr in pull_requests:
        author_name = pr.created_by.display_name

        # Ignore PRs by specified authors
        if author_name in ignored_authors:
            print(f"Ignoring PR #{pr.pull_request_id} by {author_name}")
            continue
        
        print(f"Reviewing PR #{pr.pull_request_id} - {pr.title} by {author_name}")

        # Fetch the diff content for the pull request
        diff = fetch_pr_diff(pr.pull_request_id)
        if diff:
            print(f"Fetched diff content for PR #{pr.pull_request_id}")
            
            # Analyze the diff content using OpenAI
            try:
                review_comment = analyze_pr_diff(pr.pull_request_id, diff)
                print(f"Generated Review for PR #{pr.pull_request_id}: {review_comment}")

                # Comment on the pull request with the generated feedback
                comment_on_pr(pr.pull_request_id, review_comment)
                print(f"Posted review comment on PR #{pr.pull_request_id}")
            except Exception as e:
                print(f"Error analyzing or posting comment for PR #{pr.pull_request_id}: {str(e)}")
        else:
            print(f"No diff content found for PR #{pr.pull_request_id}")


# Run the script
if __name__ == "__main__":
    review_pull_requests()
