import requests
from models.models import GithubRepoResponse


def get_github_repo_data(diagramRequest, githubRepoResponse):
    owner = diagramRequest.githubRepoOwner
    name = diagramRequest.githubRepoName

    repoURL = f"https://api.github.com/repos/{owner}/{name}"

    headers = {"Accept": "application/vnd.github+json"}

    response = requests.get(repoURL, headers=headers)

    if response.status_code == 200:
        data = response.json()

        githubRepoResponse = GithubRepoResponse()

        githubRepoResponse.githubRepoName = data["name"]
        githubRepoResponse.githubRepoOwner = data["owner"]["login"]

        print(data["name"])
        print(data["owner"]["login"])

        if diagramRequest.getLanguages:
            worked = get_github_repo_languages(diagramRequest, githubRepoResponse)

            if not worked:
                return False



        return True
    else:
        return False

def get_github_repo_languages(diagramRequest, githubRepoResponse):
    owner = diagramRequest.githubRepoOwner
    name = diagramRequest.githubRepoName

    languages_url = f"https://api.github.com/repos/{owner}/{name}/languages"
    headers = {"Accept": "application/vnd.github+json"}

    lang_response = requests.get(languages_url, headers=headers)

    if lang_response.status_code == 200:
        lang_data = lang_response.json()

        githubRepoResponse.recievedLangages = True

        sum = 0
        for lang in lang_data:
            sum += lang_data[lang]

        for lang in lang_data:
            githubRepoResponse.languages[lang] = lang_data[lang] / sum

        for key in githubRepoResponse.languages:
            print(githubRepoResponse.languages[key])

        return True
    else:
        return False