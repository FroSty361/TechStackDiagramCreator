import io
from flask import send_file
from PIL import Image, ImageDraw, ImageFont
from models.models import Diagram

# Directory Routes

LANGUAGES_IMAGES_DIRECTORY_PATH = "../static/images/languages/"

# Diagram

DIAGRAM_WIDTH = 1080
DIAGRAM_HEIGHT = 1188

def create_diagram():
    diagram = Diagram()

    diagramCanvas = create_canvas()



    diagram.canvas = diagramCanvas

    # return diagram

def serve_diagram(diagram):
    diagramCanvas = diagram.canvas

    diagramCanvasIO = io.BytesIO()

    diagramCanvas.save(diagramCanvasIO, 'PNG')

    diagramCanvasIO.seek(0)

    return send_file(diagramCanvasIO, mimetype='image/png')

def create_canvas():
    canvas = Image.new(mode="RGB", size=(DIAGRAM_WIDTH, DIAGRAM_HEIGHT), color="white")

    return canvas