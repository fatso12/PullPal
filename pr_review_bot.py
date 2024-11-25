import openai
import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Azure DevOps Organization and Project details from environment variables
organization_url = os.getenv("AZURE_ORG_URL")
personal_access_token = os.getenv("AZURE_PAT")
project_name = os.getenv("PROJECT_NAME")
repository_id = os.getenv("REPO_ID")

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
        status='all'
    )
    return pull_requests

# Analyze the PR diff using OpenAI
def analyze_pr_diff(pr_id, diff):
    prompt = f"Review the following pull request diff and provide feedback:\n{diff}"
    response = openai.Completion.create(
        model="text-davinci-003", 
        prompt=prompt, 
        max_tokens=200
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
        print(f"Reviewing PR #{pr.pull_request_id} - {pr.title}")
        diff = pr.last_merge_commit.comment  # You may want to fetch the actual diff
        if diff:
            review_comment = analyze_pr_diff(pr.pull_request_id, diff)
            print(f"Generated Review: {review_comment}")
            comment_on_pr(pr.pull_request_id, review_comment)
        else:
            print(f"No diff found for PR #{pr.pull_request_id}")

# Run the script
if __name__ == "__main__":
    review_pull_requests()
