from flask import Flask, render_template , request
from . import home
from services.githubAPI import get_github_repo_data
from models.models import DiagramRequest, DiagramLayoutRequest
from models.models import DiagramResponse
from dataclasses import dataclass, field
from typing import List, Tuple
from models.enumValues import DiagramLayouts
import datetime as dt
from services.diagramConstructor import create_diagram, serve_diagram

@dataclass
class Logging:
    logs: list[Tuple[str, str]] = field(default_factory=list)

Logging = Logging()

@home.route('/')
def index():
    return render_template("home/index.html", layouts=DiagramLayouts)

@home.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        Logging.logs.clear()

        diagramRequest = create_diagram_request(request)
        diagramResponse = DiagramResponse()

        result = get_github_repo_data(diagramRequest, diagramResponse)

        Logging.logs = Logging.logs + diagramResponse.logs # Do The First Logs First Then diagramResponese.logs So In Order

        if result == True:
            print("Hi!")

            languages = list(diagramResponse.githubRepoResponse.languages.keys())

            print(languages)

            diagram = create_diagram(diagramResponse, diagramRequest.diagramLayoutRequest)

            diagramImage = serve_diagram(diagram)

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

    diagramRequest.diagramLayoutRequest = create_diagram_layout_request(request)

    return diagramRequest

def create_diagram_layout_request(request):
    diagramLayoutRequest = DiagramLayoutRequest()

    layoutArg = request.form.get('diagramLayout')

    try:
        layout = DiagramLayouts(layoutArg)

        print(layout)

        diagramLayoutRequest.layout = layout
        return diagramLayoutRequest
    except ValueError:
        time = dt.datetime.now()

        timeString = time.strftime("%H:%M:%S")

        Logging.logs.append((f"Could Not Next Layout Type Of '{layoutArg}'. Returning Horizontal", timeString))

        diagramLayoutRequest.layout = DiagramLayouts.Horizontal
        return diagramLayoutRequest

@home.route('/logs/')
def logs_iframe():
    return render_template("home/iframe-logs.html", logs=Logging.logs)