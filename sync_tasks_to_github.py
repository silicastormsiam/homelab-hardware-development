# Metadata:
# Name of File: sync_tasks_to_github.py
# Owner: Project Manager
# Purpose: To sync tasks from application_tracking.xlsx to the RATS Project board, creating issues and attempting automated assignment to the Initiating column.
# Function: Reads tasks from application_tracking.xlsx, creates GitHub issues in silicastormsiam/homelab-hardware-development using GraphQL, and attempts to add them to the Initiating column of the RATS Project board[](https://github.com/users/silicastormsiam/projects/3) using GraphQL and REST API. Includes error handling and a manual assignment fallback.
# Version Control: Managed in Git repository: ~/homelab-hardware-development, branch: new-clean-main, hosted at https://github.com/silicastormsiam/homelab-hardware-development
# Change Log:
#   2025-07-24 07:16:00 +07: Updated script with embedded metadata and function notes for RATS task upload automation, kept related .py files.
#   2025-07-24 07:10:00 +07: Updated script with embedded metadata and function notes, removed metadata files from filesystem.
#   2025-07-24 07:06:00 +07: Updated script with embedded metadata and function notes for RATS task upload automation.
#   2025-07-24 07:00:00 +07: Updated script with embedded metadata and function notes for RATS task upload automation.

import openpyxl
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests
import os

# GitHub configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set via export GITHUB_TOKEN=your_token
REPO_NAME = "silicastormsiam/homelab-hardware-development"
PROJECT_NUMBER = 3
COLUMN_NAME = "Initiating"
USER_LOGIN = "silicastormsiam"

# Debug PAT
print(f"GITHUB_TOKEN (first 4 chars): {GITHUB_TOKEN[:4] if GITHUB_TOKEN else 'Not set'}")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not set. Run 'export GITHUB_TOKEN=your_token'.")
elif not GITHUB_TOKEN.startswith("ghp_"):
    raise ValueError("GITHUB_TOKEN invalid. Regenerate at https://github.com/settings/tokens.")

# Set up GraphQL client
transport = RequestsHTTPTransport(
    url="https://api.github.com/graphql",
    headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Load tasks from Excel
try:
    workbook = openpyxl.load_workbook("application_tracking.xlsx")
    tasks_sheet = workbook["Tasks"]
    tasks = []
    for row in tasks_sheet.iter_rows(min_row=2, values_only=True):
        tasks.append({
            "Task ID": row[0],
            "Task Name": row[1],
            "Description": row[2],
            "Process Group": row[3],
            "Due Date": row[4],
            "Status": row[5],
            "Stakeholder": row[6],
            "Priority": row[7],
            "Risks": row[8],
            "Dependencies": row[9],
            "Notes": row[10],
            "Last Updated": row[11]
        })
except FileNotFoundError:
    raise FileNotFoundError("application_tracking.xlsx not found. Run create_application_tracking.py.")

# Get repository and project IDs
try:
    query = gql("""
    query($owner: String!, $repo: String!, $userLogin: String!, $projectNumber: Int!) {
        repository(owner: $owner, name: $repo) {
            id
        }
        user(login: $userLogin) {
            projectV2(number: $projectNumber) {
                id
                title
                fields(first: 20) {
                    nodes {
                        ... on ProjectV2SingleSelectField {
                            id
                            name
                            options {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    }
    """)
    result = client.execute(query, variable_values={"owner": USER_LOGIN, "repo": "homelab-hardware-development", "userLogin": USER_LOGIN, "projectNumber": PROJECT_NUMBER})
    repo_id = result["repository"]["id"]
    print(f"Repository accessed: {REPO_NAME} (ID: {repo_id})")
    project = result["user"]["projectV2"]
    if not project:
        raise Exception(f"Project #{PROJECT_NUMBER} not found for {USER_LOGIN}.")
    project_id = result["user"]["projectV2"]["id"]
    print(f"Project accessed: {project['title']} (ID: {project_id})")

    # Find Initiating column
    status_field = next((field for field in project["fields"]["nodes"] if field["name"] == "Status"), None)
    if not status_field:
        raise Exception("Status field not found. Verify at https://github.com/users/silicastormsiam/projects/3/settings.")
    initiating_option_id = next((option["id"] for option in status_field["options"] if option["name"] == COLUMN_NAME), None)
    if not initiating_option_id:
        raise Exception(f"Column '{COLUMN_NAME}' not found. Available: {[option['name'] for option in status_field['options']]}")

    # Create issues and attempt project assignment
    for task in tasks:
        issue_body = (
            f"**Description**: {task['Description']}\n"
            f"**Process Group**: {task['Process Group']}\n"
            f"**Due Date**: {task['Due Date']}\n"
            f"**Stakeholder**: {task['Stakeholder']}\n"
            f"**Priority**: {task['Priority']}\n"
            f"**Risks**: {task['Risks']}\n"
            f"**Dependencies**: {task['Dependencies']}\n"
            f"**Last Updated**: {task['Last Updated']}\n"
            f"**Metadata Reference**: See application_tracking.xlsx in repository\n"
            f"**Note**: If not in project, manually add to Initiating column at https://github.com/users/silicastormsiam/projects/3"
        )
        # Create issue via GraphQL
        mutation = gql("""
        mutation($repositoryId: ID!, $title: String!, $body: String!, $labels: [String!]) {
            createIssue(input: {repositoryId: $repositoryId, title: $title, body: $body, labels: $labels}) {
                issue {
                    id
                    number
                    title
                }
            }
        }
        """)
        issue_result = client.execute(mutation, variable_values={
            "repositoryId": repo_id,
            "title": task["Task Name"],
            "body": issue_body,
            "labels": ["Initiating", "Task", task["Priority"]]
        })
        issue = issue_result["createIssue"]["issue"]
        print(f"Created issue: {issue['title']} (#{issue['number']}) (ID: {issue['id']})")

        # Verify issue ID
        query = gql("""
        query($issueId: ID!) {
            node(id: $issueId) {
                ... on Issue {
                    id
                    number
                    title
                }
            }
        }
        """)
        verify_result = client.execute(query, variable_values={"issueId": issue["id"]})
        if not verify_result["node"]:
            print(f"Warning: Issue ID {issue['id']} not found. Skipping project assignment.")
            continue
        print(f"Verified issue ID: {issue['id']} for issue #{issue['number']}")

        # Try GraphQL project assignment
        try:
            mutation = gql("""
            mutation($projectId: ID!, $contentId: ID!) {
                addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                    item {
                        id
                    }
                }
            }
            """)
            add_result = client.execute(mutation, variable_values={
                "projectId": project_id,
                "contentId": issue["id"]
            })
            item_id = add_result["addProjectV2ItemById"]["item"]["id"]
            print(f"Added issue #{issue['number']} to project (Item ID: {item_id})")

            # Update status to Initiating
            mutation = gql("""
            mutation($projectId: ID!, $itemId: ID!, $statusFieldId: ID!, $statusValueId: ID!) {
                updateProjectV2ItemFieldValue(input: {
                    projectId: $projectId
                    itemId: $itemId
                    fieldId: $statusFieldId
                    value: {singleSelectOptionId: $statusValueId}
                }) {
                    projectV2Item {
                        id
                    }
                }
            }
            """)
            client.execute(mutation, variable_values={
                "projectId": project_id,
                "itemId": item_id,
                "statusFieldId": status_field["id"],
                "statusValueId": initiating_option_id
            })
            print(f"Set issue #{issue['number']} to Initiating column.")
        except Exception as e:
            print(f"GraphQL project assignment failed for issue #{issue['number']}: {str(e)}")
            # Fallback to REST API
            try:
                headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
                project_url = f"https://api.github.com/projects/{project_id}/cards"
                response = requests.post(project_url, headers=headers, json={
                    "content_id": int(issue["number"]),  # REST API uses issue number
                    "content_type": "Issue"
                })
                if response.status_code == 201:
                    print(f"Added issue #{issue['number']} to project via REST API.")
                else:
                    print(f"REST API failed: {response.status_code} {response.text}. Manually add issue #{issue['number']} to Initiating column at https://github.com/users/silicastormsiam/projects/3.")
            except Exception as rest_e:
                print(f"REST API project assignment failed: {str(rest_e)}. Manually add issue #{issue['number']} to Initiating column at https://github.com/users/silicastormsiam/projects/3.")

except Exception as e:
    print(f"Error: {str(e)}")
    if "401" in str(e):
        print("401 Bad Credentials: Verify GITHUB_TOKEN at https://github.com/settings/tokens.")
    elif "404" in str(e):
        print(f"404 Not Found: Verify REPO_NAME ({REPO_NAME}), USER_LOGIN ({USER_LOGIN}), or project details at https://github.com/users/silicastormsiam/projects/3.")
    raise

print("Tasks processed. Check issues at https://github.com/silicastormsiam/homelab-hardware-development/issues and project board at https://github.com/users/silicastormsiam/projects/3.")
