from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from PIL import Image
from .enumValues import DiagramLayouts

@dataclass
class DiagramLayoutRequest:
    layout = DiagramLayouts.Horizontal

@dataclass
class DiagramRequest:
    # Repo

    githubRepoOwner: str = ""
    githubRepoName: str = ""

    # Search Behaviors

    getLanguages: bool = False
    getRequirements: bool = False

    # Layout

    diagramLayoutRequest: DiagramLayoutRequest = field(default_factory=DiagramLayoutRequest)

@dataclass
class GithubRepoResponse:
    # Repo

    githubRepoOwner: str = ""
    githubRepoName: str = ""

    # Languages

    recievedLangages: bool = False
    languages: Dict[str, float] = field(default_factory=dict)

    # Requirements

    recievedRequirements: bool = False
    requirements = []

@dataclass
class DiagramResponse:
    # Github Specific Data

    githubRepoResponse: GithubRepoResponse = field(default_factory=GithubRepoResponse)

    # Logging

    logs: list[Tuple[str, str]] = field(default_factory=list)

# Result

@dataclass
class Diagram:
    def __init__(self):
        self.canvas: Image = field(default_factory=Image)

        self.width: int = 0
        self.height: int = 0

        self.totalArea: int = 0
        self.remainingArea: float = 0