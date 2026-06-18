import base64
import io
import os
from typing import Dict
from flask import send_file
from PIL import Image, ImageDraw, ImageFont
from models.models import Diagram, GithubRepoResponse
from models.enumValues import DiagramLayouts
import math

# Directory Routes

LANGUAGES_IMAGES_DIRECTORY_PATH = "app/static/images/languages/"
REQUIREMENTS_IMAGES_DIRECTORY_PATH = "app/static/images/requirements/"

# Diagram

DIAGRAM_WIDTH = 1080
DIAGRAM_HEIGHT = 1188

def create_diagram(diagramResponse, diagramLayoutRequest):
    diagram = Diagram

    diagram.width = DIAGRAM_WIDTH
    diagram.height = DIAGRAM_HEIGHT

    diagramCanvas = create_canvas()

    if diagramResponse.githubRepoResponse.recievedLangages == False and diagramResponse.githubRepoResponse.recievedRequirements == False:
        print("No Languages And No Requirements Were Received")

        return None

    if diagramResponse.githubRepoResponse.recievedLangages and diagramResponse.githubRepoResponse.recievedRequirements:
        languagesAmount = len(diagramResponse.githubRepoResponse.languages.keys())
        requirementsAmount = len(diagramResponse.githubRepoResponse.requirements)

        languagesToRequirementsRatio = languagesAmount / (languagesAmount + requirementsAmount)

        languagesSize = (diagram.width, diagram.height)
        requirementsSize = (diagram.width, diagram.height)

        match diagramLayoutRequest.layout:
            case DiagramLayouts.Horizontal:
                languagesSize = (int(diagram.width), int(diagram.height * languagesToRequirementsRatio))
                requirementsSize = (int(diagram.width), int(diagram.height * (1 - languagesToRequirementsRatio)))
            case DiagramLayouts.Vertical:
                languagesSize = (int(diagram.width * languagesToRequirementsRatio), int(diagram.height))
                requirementsSize = (int(diagram.width * (1 - languagesToRequirementsRatio)), int(diagram.height))

        languagesSection = create_diagram_languages_section(languagesSize, diagramResponse.githubRepoResponse.languages)
        requirementsSection = create_diagram_requirements_section(requirementsSize)

        diagramCanvas.paste(languagesSection, (0, 0))
        diagramCanvas.paste(requirementsSection, (0, int(languagesSection.height)))

    diagram.canvas = diagramCanvas

    return diagram

def serve_diagram(diagram):
    diagramCanvas = diagram.canvas
    diagramCanvasIO = io.BytesIO()
    diagramCanvas.save(diagramCanvasIO, 'PNG')
    diagramCanvasIO.seek(0)

    image_data = diagramCanvasIO.getvalue()
    base64_string = base64.b64encode(image_data).decode('utf-8')

    return base64_string

def create_canvas():
    canvas = Image.new(mode="RGB", size=(DIAGRAM_WIDTH, DIAGRAM_HEIGHT), color="white")

    return canvas

# Sections

def create_diagram_languages_section(size, languages: Dict[str, float]):
    canvas = Image.new(mode="RGB", size=size, color="aqua")

    if not languages:
        return canvas

    icon_size_width = int(size[0] / len(languages))
    icon_size_height = int(size[1] / len(languages))

    xPos = 0
    yPos = 0

    for language, value in languages.items():
        image_path = os.path.join(LANGUAGES_IMAGES_DIRECTORY_PATH, f"{language}.png")

        try:
            language_image = Image.open(image_path)

            language_image.thumbnail((icon_size_width, icon_size_height), Image.Resampling.LANCZOS)

            if language_image.mode == 'P':
                transparency = language_image.info.get("transparency")

                if isinstance(transparency, bytes):
                    language_image = language_image.convert('RGBA')

            if language_image.mode in ('RGBA', 'LA'):
                canvas.paste(language_image, (int(xPos), int(yPos)), language_image)
            else:
                canvas.paste(language_image, (int(xPos), int(yPos)))

            xPos += icon_size_width

            if xPos + icon_size_width > size[0]:
                xPos = 0
                yPos += icon_size_height

                if yPos + icon_size_height > size[1]:
                    break

        except FileNotFoundError:
            print(f"Image Not Found For Path {language}")

    return canvas

def create_diagram_requirements_section(size):
    canvas = Image.new(mode="RGB", size=size, color="blue")

    return canvas