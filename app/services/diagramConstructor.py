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
    diagram = Diagram()

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
        requirementsSection = create_diagram_requirements_section(requirementsSize, diagramResponse.githubRepoResponse.requirements)

        match diagramLayoutRequest.layout:
            case DiagramLayouts.Horizontal:
                diagramCanvas.paste(languagesSection, (0, 0))
                diagramCanvas.paste(requirementsSection, (0, int(languagesSection.height)))
            case DiagramLayouts.Vertical:
                diagramCanvas.paste(languagesSection, (0, 0))
                diagramCanvas.paste(requirementsSection, (int(languagesSection.width), 0))

    elif diagramResponse.githubRepoResponse.recievedLangages and diagramResponse.githubRepoResponse.recievedRequirements == False:
        languagesSection = create_diagram_languages_section((diagram.width, diagram.height), diagramResponse.githubRepoResponse.languages)

        diagramCanvas.paste(languagesSection, (0, 0))
    elif diagramResponse.githubRepoResponse.recievedRequirements and diagramResponse.githubRepoResponse.recievedLangages== False:
        requirementsSection = create_diagram_requirements_section((diagram.width, diagram.height), diagramResponse.githubRepoResponse.requirements)

        diagramCanvas.paste(requirementsSection, (0, 0))

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

    amount = len(languages)

    cols = max(1, math.ceil(math.sqrt(amount)))
    rows = max(1, math.ceil(amount / cols))

    icon_width = size[0] // cols
    icon_height = size[1] // rows

    xPos = 0
    yPos = 0
    i = 0

    for language, value in languages.items():
        image_path = os.path.join(LANGUAGES_IMAGES_DIRECTORY_PATH, f"{language}.png")
        image_path = image_path.replace('*', "star")

        try:
            language_image = Image.open(image_path)

            image_width = language_image.size[0]
            image_height = language_image.size[1]
            ratio = min(icon_width / image_width, icon_height / image_height)
            new_width = int(image_width * ratio)
            new_height = int(image_height * ratio)

            language_image = language_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            x_offset = int(xPos + (icon_width - new_width) // 2)
            y_offset = int(yPos + (icon_height - new_height) // 2)

            if language_image.mode == 'P':
                transparency = language_image.info.get("transparency")

                if isinstance(transparency, bytes):
                    language_image = language_image.convert('RGBA')

            if language_image.mode in ('RGBA', 'LA'):
                canvas.paste(language_image, (x_offset, y_offset), language_image)
            else:
                canvas.paste(language_image, (x_offset, y_offset))

            xPos += icon_width
            i += 1

            if i % cols == 0:
                xPos = 0
                yPos += icon_height

        except FileNotFoundError:
            print(f"Image Not Found For {language}")

    return canvas

def create_diagram_requirements_section(size, requirements: list[str]):
    canvas = Image.new(mode="RGB", size=size, color="blue")

    if not requirements:
        return canvas

    amount = len(requirements)

    cols = max(1, math.ceil(math.sqrt(amount)))
    rows = max(1, math.ceil(amount / cols))

    icon_width = size[0] // cols
    icon_height = size[1] // rows

    xPos = 0
    yPos = 0
    i = 0

    for requirement in requirements:
        image_path = os.path.join(REQUIREMENTS_IMAGES_DIRECTORY_PATH, f"{requirement}.png")
        image_path = image_path.replace('*', "star")

        try:
            requirement_image = Image.open(image_path)

            image_width = requirement_image.size[0]
            image_height = requirement_image.size[1]
            ratio = min(icon_width / image_width, icon_height / image_height)
            new_width = int(image_width * ratio)
            new_height = int(image_height * ratio)

            requirement_image = requirement_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            x_offset = int(xPos + (icon_width - new_width) // 2)
            y_offset = int(yPos + (icon_height - new_height) // 2)

            if requirement_image.mode == 'P':
                transparency = requirement_image.info.get("transparency")

                if isinstance(transparency, bytes):
                    requirement_image = requirement_image.convert('RGBA')

            if requirement_image.mode in ('RGBA', 'LA'):
                canvas.paste(requirement_image, (x_offset, y_offset), requirement_image)
            else:
                canvas.paste(requirement_image, (x_offset, y_offset))

            xPos += icon_width
            i += 1

            if i % cols == 0:
                xPos = 0
                yPos += icon_height

        except FileNotFoundError:
            print(f"Image Not Found For {requirement}")

    return canvas