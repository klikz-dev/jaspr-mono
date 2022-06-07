"""
This script relaunches the scheduler Fargate instance with Env Vars
that tell the process to dump specific fixtures and send them to the fixture S3 bucket.

@arg1 Name of the current deployment (release, integration, production)
@arg2 List of Fixtures to load. Should be a list of URL paths to S3 with semicolonsas a delimiter.
(ex. "s3://jaspr-integration-fixtures/import/content.json;s3://jaspr-integration-fixtures/import/task.json")
"""

import os
import sys
import json
from os.path import abspath

DEPLOYMENT_NAME = sys.argv[1]
DEFINITION_NAME = "jaspr-scheduler"

# This should really be pulled from terraforms output variables.
if DEPLOYMENT_NAME == "release":
    CLUSTER_NAME = f"scheduler-cluster-development-{DEPLOYMENT_NAME}"
    SERVICE_NAME = f"scheduler-development-{DEPLOYMENT_NAME}"
else:
    CLUSTER_NAME = f"scheduler-cluster-{DEPLOYMENT_NAME}"
    SERVICE_NAME = f"scheduler-{DEPLOYMENT_NAME}"

FILE_PATH = abspath("./scheduler-save-fixtures-definition-no-collision.json")


# Get current Task for the cluster
GET_TASK_COMMAND = f'aws ecs list-tasks --cluster {CLUSTER_NAME} --region us-west-1'
with os.popen(GET_TASK_COMMAND) as stream:
    task_list = json.load(stream)
    task_arn = task_list["taskArns"][0]

GET_LIST_TASK_COMMAND = f"aws ecs describe-tasks --cluster {CLUSTER_NAME} --tasks {task_arn} --region us-west-1"
with os.popen(GET_LIST_TASK_COMMAND) as stream:
    task_desc = json.load(stream)
    task_definition_arn = task_desc["tasks"][0]["taskDefinitionArn"]

# Get current Task Definition for scheduler
GET_TASK_DEF_COMMAND = f'aws ecs describe-task-definition --task-definition {task_definition_arn} --region us-west-1'
with os.popen(GET_TASK_DEF_COMMAND) as stream:
    task_def = json.load(stream)
    task_def = task_def["taskDefinition"]

# Update Task Definition String to include Fixture List
stripped_fields = [
    "taskDefinitionArn",
    "revision",
    "status",
    "requiresAttributes",
    "compatibilities",
    "registeredAt", #
    "registeredBy", #
]
for field in stripped_fields:
    task_def.pop(field)

found = False
for item in task_def["containerDefinitions"][0]["environment"]:
    if item["name"] == "SAVE_FIXTURES":
        item["value"] = "True"
        found = True

if not found:
    task_def["containerDefinitions"][0]["environment"].append({
        "name": "SAVE_FIXTURES",
        "value": "True"
    })


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