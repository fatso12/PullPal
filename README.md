

![alt text](https://i.ibb.co/c2Fqyp7/IMG-7647.png)

## AI-Powered Pull Request Reviewer 🚀

PullPal combines the capabilities of OpenAI 🧠 and Azure DevOps ⚙️ to automate the review process for pull requests.
It periodically fetches active pull requests from Azure DevOps, analyzes the code changes using OpenAI's specified model,
and posts the review comments directly on the pull request threads.


How to Use:

## Set up Environment Variables:

Create a .env file in the project root.
## Add the following environment variables:
OPENAI_API_KEY: Your OpenAI API key.

AZURE_ORG_URL: Your Azure DevOps organization URL.

AZURE_PAT: Your Azure DevOps Personal Access Token.

PROJECT_NAME: Your Azure DevOps project name.

REPO_ID: Your Azure DevOps repository ID.

IGNORED_AUTHORS: A comma-separated list of authors to ignore.

INTERVAL_HOURS: running interval for fetching the PR's

## Run the Script 🏃‍♂️

To run the PullPal bot continuously using Docker, follow these steps:

1. **Build the Docker Image 🛠️:**
```sh
   docker build -t pullpal-bot .
   ```
2.**Run the Docker Container 🐋:**
```sh
docker run -d --env-file .env pullpal-bot
```

Customization:

check .env file for customization,prompt is hardcoded but fill free to adjust



 ## Feel free to fork the repository, make changes, and submit a pull request - issues are available !

MIT License
