# Azure DevOps PR Review Bot

This bot automatically reviews pull requests (PRs) in Azure DevOps and generates feedback using OpenAI's GPT model. The bot fetches pull request details, analyzes the diffs, and posts comments with a review. It is deployed on AWS and can be triggered periodically or on-demand.

## Features

- Fetches all pull requests from an Azure DevOps repository.
- Analyzes the PR diffs using OpenAI's GPT model.
- Posts feedback as comments on the PR.
- Uses environment variables to securely store API keys and configuration.

## AWS Services Used

### 1. **AWS Lambda (Recommended)**

The bot is designed to run as an AWS Lambda function. AWS Lambda allows you to run the code without provisioning or managing servers. Lambda will execute the bot on a scheduled basis or based on an event (e.g., when a new PR is created).

### 2. **Amazon CloudWatch Events (for Scheduling)**

CloudWatch Events can trigger the Lambda function to run at specified intervals (e.g., every hour, every day). This allows the bot to automatically review PRs without manual intervention.

### 3. **AWS Secrets Manager (Optional)**

For enhanced security, AWS Secrets Manager can be used to securely store sensitive information like API keys (OpenAI API key, Azure PAT). You can retrieve these secrets directly in your Lambda function.

## Requirements

- Python 3.x
- Azure DevOps Personal Access Token (PAT)
- OpenAI API Key
- AWS Account for deploying the bot

### Python Libraries

This bot uses the following libraries:
- `azure-devops`: To interact with the Azure DevOps API.
- `openai`: To interact with the OpenAI API.
- `requests`: For making HTTP requests.
- `python-dotenv`: To load environment variables from a `.env` file.

### Install Dependencies

To install the necessary Python libraries, run:

```bash
pip install -r requirements.txt
```
### Configuration
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key
AZURE_ORG_URL=https://dev.azure.com/your_organization
AZURE_PAT=your_azure_pat
PROJECT_NAME=your_project_name
REPO_ID=your_repo_id
```



