import sys
import subprocess
import re

PATTERN = "commit ([a-z0-9]+)"
REGEX = re.compile(PATTERN, re.MULTILINE)


def git(command):
    command = ["git"] + command
    output = subprocess.run(command, stdout=subprocess.PIPE, check=True)
    return output.stdout.decode('utf-8')


def does_branch_exist(git_branch):
    result = git(["branch", "--list", git_branch])
    return result.find(git_branch) > -1


def find_last_git_commit(git_branch):
    try:
        git_log = git(["log", "--all", "--grep", f"Merged in {git_branch}"])
        result = REGEX.match(git_log)
        return result.groups("1")[0]
    except Exception as e:
        raise Exception(f"Could not find commit for git branch. Exception: {e}")


def checkout_ref(git_ref):
    try:
        git(["checkout", git_ref])
    except Exception as e:
        raise Exception(f"Could not checkout commit hash: {git_ref}. Exception: {e}")


def checkout_name(git_branch):
    try:
        git(["checkout", "-b", git_branch])
    except Exception as e:
        raise Exception(f"Could not checkout git branch: {git_branch}. Exception: {e}")


def pull_branch(git_branch):
    try:
        git(["pull", "origin", git_branch])
    except Exception as e:
        pass


def main(git_branch):
    if does_branch_exist(git_branch):
        print("branch exists.")
        checkout_ref(git_branch)
        pull_branch(git_branch)

    print("branch has been deleted.")
    git_hash = find_last_git_commit(git_branch)
    checkout_ref(git_hash)
    checkout_name(git_branch)

    print("executing terraform destroy")
    
    # execute /destroy
    print("complete")


if __name__ == "__main__":
    main(sys.argv[1])
