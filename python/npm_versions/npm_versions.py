import subprocess
import sys

import requests

registry_url = "https://registry.npmjs.org"


def get_package_versions(package_name):
    package_url = f"{registry_url}/{package_name}"
    response = requests.get(package_url)

    if response.status_code == 200:
        package_info = response.json()
        return list(package_info["versions"].keys())
    else:
        print(f"Failed to fetch versions. Status code: {response.status_code}")
        return None


def download_package_versions(package_name):
    versions = get_package_versions(package_name)

    if versions:
        print(f"Downloading all available versions for {package_name}: ")
        for version in versions:
            subprocess.run(
                [
                    "npm",
                    "pack",
                    f"{package_name}@{version}",
                    "--registry",
                    f"{registry_url}",
                ]
            )
    else:
        print(f"No versions available for {package_name}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <get/download> <package_name>")
        sys.exit(1)

    action = sys.argv[1]
    package_name = sys.argv[2]

    if action == "get":
        versions = get_package_versions(package_name)
        if versions:
            print(f"Versions available for {package_name}: ")
            for version in versions:
                print(version)
    elif action == "download":
        download_package_versions(package_name)
    else:
        print("Invalid action. Use 'get' or 'download'.")
