import requests

def get_github_repo(owner, name):
    repoURL = f"https://api.github.com/repos/{owner}/{name}"

    response = requests.get(repoURL)

    if response.status_code == 200:
        data = response.json()

        print(data["name"])
        print(data["owner"]["login"])
        print(data["description"])

        return data
    else:
        return {"message": "Not Found"}