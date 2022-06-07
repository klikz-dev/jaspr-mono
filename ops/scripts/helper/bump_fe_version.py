"""
This script sets the AppStore version for Android and iOS frontend builds to the BITBUCKET_BUILD_NUMBER Env Var.
"""

import json
import os
import sys

JAH_APP_JSON_FILE_PATH = "../../../jah/app.json"
JAH_PACKAGE_JSON_FILE_PATH = "../../../jah/package.json"
FRONTEND_PACKAGE_JSON_FILE_PATH = "../../../frontend/package.json"


def main():
    print("Starting FE Version Bump...")
    print(sys.argv)

    if len(sys.argv) < 3:
        raise Exception("Missing arguments.")

    build_number = sys.argv[1]
    software_version = sys.argv[2]

    appjson = None
    with open(JAH_APP_JSON_FILE_PATH, "r") as f:
        appjson = json.load(f)
    prev_ios_version = int(appjson["expo"]["ios"]["buildNumber"])
    new_ios_version = build_number
    appjson["expo"]["ios"]["buildNumber"] = str(new_ios_version)
    print(f"Bumping iOS version: {prev_ios_version} -> {new_ios_version}")

    prev_android_version = appjson["expo"]["android"]["versionCode"]
    new_android_version = build_number
    appjson["expo"]["android"]["versionCode"] = int(new_android_version)
    print(
        f"Bumping Android version: {prev_android_version} -> {new_android_version}")

    with open(JAH_APP_JSON_FILE_PATH, "w") as f:
        json.dump(appjson, f, indent=4)

    if software_version != "0":
        print(
            f"Bumping software version in package.json to {software_version}")

        # JAH
        jah_package_json = None
        with open(JAH_PACKAGE_JSON_FILE_PATH, "r") as f:
            jah_package_json = json.load(f)

        jah_package_json["version"] = software_version

        with open(JAH_PACKAGE_JSON_FILE_PATH, "w") as f:
            json.dump(jah_package_json, f, indent=4)

        # Frontend
        frontend_package_json = None
        with open(FRONTEND_PACKAGE_JSON_FILE_PATH, "r") as f:
            frontend_package_json = json.load(f)

        frontend_package_json["version"] = software_version

        with open(FRONTEND_PACKAGE_JSON_FILE_PATH, "w") as f:
            json.dump(frontend_package_json, f, indent=4)
    else:
        print("Skipping Software Version Bump in package.json")

    print("Finished FE Version Bump.")


if __name__ == "__main__":
    main()
