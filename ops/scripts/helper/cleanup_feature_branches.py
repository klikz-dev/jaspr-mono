import sys
import subprocess

import boto3
import requests

s3 = boto3.client('s3')
DEVELOPMENT_TERRAFORM_BUCKET = "jaspr-terraform-state-development"
IGNORE_LIST = [
    "base-terraform",
    "release"
]
BITBUCKET_WORKSPACE = "ebpi"
BITBUCKET_REPO_SLUG = "jaspr-mono"
BITBUCKET_URL = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests"
BB_USERNAME = "todd-cullen"
BB_PWD = "PqL4a6bXhEyrcxBZ9GaY" # read only password to BB Pull Requests


# Get list of active branches from S3
def get_feature_branches():
    '''
    Get list of active branches from S3.
    Exclude branches that have already been torn down. They can be found by their small file size (less than 200B).
    :return: list of feature branch names
    '''
    feature_branches = []
    response = s3.list_objects(Bucket=DEVELOPMENT_TERRAFORM_BUCKET)
    for item in response["Contents"]:
        key = item['Key'].replace(".tfstate", "")
        if key not in IGNORE_LIST and item['Size'] > 200:
            feature_branches.append(key)
    return feature_branches


# Get list of open PRs from Bitbucket
def get_open_prs():
    prs = []
    next_url = BITBUCKET_URL
    while True:
        r = requests.get(next_url, auth = (BB_USERNAME, BB_PWD))
        data = r.json()
        for pr in data["values"]:
            prs.append(pr["source"]["branch"]["name"])
        if "next" not in data:
            break
        next_url = data["next"]
    return prs


# find branches that don't have PRs
def get_inactive_deployments():
    feature_branches = get_feature_branches()
    prs = get_open_prs()
    result = []
    for branch in feature_branches:
        if branch not in prs:
            result.append(branch)
    return result


def cmd(command, cwd=None):
    output = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, cwd=cwd)
    for line in iter(output.stdout.readline, b''):
        sys.stdout.write(line.decode(sys.stdout.encoding))


def git(command):
    cmd(["git"] + command)


def main():
    deployments = get_inactive_deployments()
    print("\nFeature Branches For Removal")
    print("---------------------------------------")
    for branch in deployments:
        print(branch)
    print("---------------------------------------")
    result = input("Do you want to teardown these branches? (y/n): ")
    if result != "y":
        print("Exiting process.")
        sys.exit(0)
    print("Starting feature branch deletion...")
    for deployment in deployments:
        print(f"Processing {deployment}...")
        try:
            git(["branch", "-d", deployment])
        except:
            print("Branch does not exist")
        git(["checkout", "release"])
        git(["branch", deployment])
        git(["checkout", deployment])
        cmd(["./destroy.sh", "dev"], cwd="../deployment")
        git(["checkout", "release"])
        print(f"Finished with {deployment}")
    print("Complete.")

if __name__ == "__main__":
    main()
