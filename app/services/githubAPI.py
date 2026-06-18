import requests
from models.models import GithubRepoResponse, DiagramResponse
import base64
import datetime as dt

def get_github_repo_data(diagramRequest, diagramResponse):
    owner = diagramRequest.githubRepoOwner
    name = diagramRequest.githubRepoName

    repoURL = f"https://api.github.com/repos/{owner}/{name}"

    headers = {"Accept": "application/vnd.github+json"}

    response = requests.get(repoURL, headers=headers)

    if response.status_code == 200:
        data = response.json()

        diagramResponse.githubRepoResponse.githubRepoName = data["name"]
        diagramResponse.githubRepoResponse.githubRepoOwner = data["owner"]["login"]

        print(data["name"])
        print(data["owner"]["login"])

        if diagramRequest.getLanguages:
            worked = get_github_repo_languages(diagramRequest, diagramResponse)

            if not worked:
                time = dt.datetime.now()

                timeString = time.strftime("%H:%M:%S")

                diagramResponse.logs.append((f"Could Not Get GitHub Langauges For Repository '{owner}/{name}'", timeString))

        if diagramRequest.getRequirements:
            worked = get_github_repo_requirements(diagramRequest, diagramResponse)

            if not worked:
                time = dt.datetime.now()

                timeString = time.strftime("%H:%M:%S")

                diagramResponse.logs.append((f"Could Not Get GitHub Requirements For Repository '{owner}/{name}'", timeString))

        return True
    else:
        time = dt.datetime.now()

        timeString = time.strftime("%H:%M:%S")

        diagramResponse.logs.append((f"Could Not Get GitHub Repository '{owner}/{name}'", timeString))

        return False

def get_github_repo_languages(diagramRequest, diagramResponse):
    owner = diagramRequest.githubRepoOwner
    name = diagramRequest.githubRepoName

    languages_url = f"https://api.github.com/repos/{owner}/{name}/languages"
    headers = {"Accept": "application/vnd.github+json"}

    lang_response = requests.get(languages_url, headers=headers)

    if lang_response.status_code == 200:
        lang_data = lang_response.json()

        if len(lang_data) > 0:
            diagramResponse.githubRepoResponse.recievedLangages = True

        sum = 0
        for lang in lang_data:
            sum += lang_data[lang]

        for lang in lang_data:
            diagramResponse.githubRepoResponse.languages[lang] = lang_data[lang] / sum

        return True
    else:
        return False

def get_github_repo_requirements(diagramRequest, diagramResponse):
    owner = diagramRequest.githubRepoOwner
    name = diagramRequest.githubRepoName

    requirmenrs_url = f"https://api.github.com/repos/{owner}/{name}/contents/requirements.txt"
    headers = {"Accept": "application/vnd.github+json"}

    req_response = requests.get(requirmenrs_url, headers=headers)

    if req_response.status_code == 200:
        data = req_response.json()
        encodedContent = data.get("content", "")

        contentBytes = base64.b64decode(encodedContent)
        content = contentBytes.decode("utf-8")

        lines = content.split("\n")

        if len(lines) > 0:
            diagramResponse.githubRepoResponse.recievedRequirements = True

        for line in lines:
            index = line.find("=")
            if index == -1:
                index = line.find("~")

            if index != -1:
                requirement = line[:index - 1]

                diagramResponse.githubRepoResponse.requirements.append(requirement)

        for req in diagramResponse.githubRepoResponse.requirements:
            print(req)

        return True
    else:
        return False