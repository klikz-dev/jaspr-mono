"""
This script relaunches the scheduler Fargate instance with Env Vars
that tell the process to load fixture data from S3.

@arg1 Name of the current deployment, expects either integration or production
@arg2 List of Fixtures to load. Should be a list of URL paths to S3 with semicolonsas a delimiter.
(ex. "s3://jaspr-integration-fixtures/import/content.json;s3://jaspr-integration-fixtures/import/task.json")
"""

import os
import sys
import json
from os.path import abspath

DEPLOYMENT_NAME = sys.argv[1]
if DEPLOYMENT_NAME not in ("integration", "production"):
    print("Invalid Deployment. Must be either integration or production")
    sys.exit(1)

DEFINITION_NAME = "jaspr-scheduler"
CLUSTER_NAME = f"scheduler-cluster-{DEPLOYMENT_NAME}"
SERVICE_NAME = f"scheduler-{DEPLOYMENT_NAME}"
FILE_PATH = abspath("./scheduler_definition-no-collision.json")

# Get current Task Definition for scheduler
GET_TASK_DEF_COMMAND = f'aws ecs describe-task-definition --task-definition {DEFINITION_NAME} --region us-west-1'
with os.popen(GET_TASK_DEF_COMMAND) as stream:
    task_def = json.load(stream)
    task_def = task_def["taskDefinition"]

# Update Task Definition String to include Fixture List
stripped_fields = [
    "taskDefinitionArn",
    "revision",
    "status",
    "requiresAttributes",
    "compatibilities"
]
for field in stripped_fields:
    task_def.pop(field)

for item in task_def["containerDefinitions"][0]["environment"]:
    if item["name"] == "GENERATE_STATIC_TOKEN":
        item["value"] = "True"
    # This is currently already set in the env vars
    #if item["name"] == "STATIC_TOKEN_USER":
    #    item["value"] = "dev@jasprhealth.com"

with open(FILE_PATH, "w") as f:
    json.dump(task_def, f)

UPDATE_TASK_COMMAND = f'aws ecs register-task-definition --cli-input-json file://{FILE_PATH} --region us-west-1'
with os.popen(UPDATE_TASK_COMMAND) as stream:
    output = stream.read()

print("Update Task Def Output.....")
print(output)

# Update service for scheduler to latest version
UPDATE_SERVICE_COMMAND = f'aws ecs update-service --cluster {CLUSTER_NAME} --service {SERVICE_NAME} --task-definition {DEFINITION_NAME} --region us-west-1'
with os.popen(UPDATE_SERVICE_COMMAND) as stream:
    output = stream.read()

print("Update Service Output.....")
print(output)