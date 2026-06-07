class DiagramRequest:
    # Repo

    githubRepoOwner = ""
    githubRepoName = ""

    # Search Behaviors

    getLanguages = True
    readRequirements = True

    # Design

class DiagramResponse:
    # Github Specific Data

    GithubRepoResponse = None

class GithubRepoResponse:
    # Repo

    githubRepoOwner = ""
    githubRepoName = ""

    # Languages

    recievedLangages = False

    languages = {
        # "language": percentage
    }

    # Requirements

    recievedRequirements = False