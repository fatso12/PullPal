import openai
import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Azure DevOps Organization and Project details from environment variables
organization_url = os.getenv("AZURE_ORG_URL")
personal_access_token = os.getenv("AZURE_PAT")
project_name = os.getenv("PROJECT_NAME")
repository_id = os.getenv("REPO_ID")

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
    git_client = connection.clients.get_git_client()
    pull_requests = git_client.get_pull_requests(
        project=project_name,
        repository_id=repository_id,
        status='active'
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
        model="text-davinci-003", 
        prompt=prompt, 
        max_tokens=300
    )
    return response.choices[0].text.strip()

# Comment on the pull request
def comment_on_pr(pr_id, comment):
    connection = get_azure_devops_connection()
    git_client = connection.clients.get_git_client()
    git_client.create_comment(
        project=project_name,
        repository_id=repository_id,
        pull_request_id=pr_id,
        comment={'content': comment}
    )

# Main function to fetch PRs and review them
def review_pull_requests():
    pull_requests = get_pull_requests()
    for pr in pull_requests:
        pr_author = pr.created_by.display_name
        pr_creation_date = pr.creation_date  # ISO 8601 format
        pr_id = pr.pull_request_id

        # Skip ignored authors
        if is_author_ignored(pr_author):
            print(f"Skipping PR #{pr_id} by ignored author: {pr_author}")
            continue

        # Skip PRs older than 24 hours
        if not is_recent_pr(pr_creation_date):
            print(f"Skipping PR #{pr_id} - not created within the last 24 hours")
            continue

        print(f"Reviewing PR #{pr_id} by {pr_author} - {pr.title}")
        diff = pr.last_merge_commit.comment  # Fetch the actual diff here
        if diff:
            review_comment = analyze_pr_diff(pr_id, diff)
            print(f"Generated Review: {review_comment}")
            comment_on_pr(pr_id, review_comment)
        else:
            print(f"No diff found for PR #{pr_id}")

# Run the script
if __name__ == "__main__":
    review_pull_requests()
