from flask import Flask, render_template , request
from . import home
from services.githubAPI import get_github_repo_data
from models.models import DiagramRequest
from models.models import DiagramResponse
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Logging:
    logs: list[Tuple[str, str]] = field(default_factory=list)

Logging = Logging()

@home.route('/')
def index():
    return render_template("home/index.html")

@home.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        diagramRequest = create_diagram_request(request)
        diagramResponse = DiagramResponse()

        result = get_github_repo_data(diagramRequest, diagramResponse)

        Logging.logs = diagramResponse.logs

        if result:
            print("Hi!")

            languages = list(diagramResponse.githubRepoResponse.languages.keys())

            print(languages)

            return render_template("home/result.html", response="Results Found!", languages=languages)

    return render_template("home/result.html", response="Could Not Get Results")

def create_diagram_request(request):
    diagramRequest = DiagramRequest()

    diagramRequest.githubRepoOwner = request.form['repoOwner']
    diagramRequest.githubRepoName = request.form['repoName']

    getLanguagesValue = request.form.get('getLanguages')
    if getLanguagesValue == 'true':
        diagramRequest.getLanguages = True
    else:
        diagramRequest.getLanguages = False

    getRequirementsValue = request.form.get('getRequirements')
    if getRequirementsValue == 'true':
        diagramRequest.getRequirements = True
    else:
        diagramRequest.getRequirements = False

    return diagramRequest

@home.route('/logs/')
def logs_iframe():
    return render_template("home/iframe-logs.html", logs=Logging.logs)