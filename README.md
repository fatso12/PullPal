

# PullPal 🤖
![alt text](https://ibb.co/L9tK0q2)
## AI-Powered Pull Request Reviewer 🚀

PullPal leverages the power of OpenAI 🧠 and Azure DevOps ⚙️ to automate the review process for pull requests. 
By analyzing code changes and providing actionable feedback using OpenAI, 
it helps maintain clean code quality and accelerate development by providing code review comments.

## Features:

Automated Code Review 🤖: Analyzes pull request diffs using OpenAI's advanced language models.

Customizable Feedback 📝: Tailors feedback to specific code quality metrics and style guidelines.

Azure DevOps Integration 🔗: Seamlessly integrates with Azure DevOps to fetch and comment on pull requests.

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
Run the Script:

Execute the review_pull_requests() function to initiate the review process.
Customization:

Modify the analyze_pr_diff function to customize the prompt and feedback generation.
Adjust the is_recent_pr function to change the time window for PR consideration.
Extend the IGNORED_AUTHORS list to exclude specific authors.




 ## Feel free to fork the repository, make changes, and submit a pull request - issues are available !

MIT License
