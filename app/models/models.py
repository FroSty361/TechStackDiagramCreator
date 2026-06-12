from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from PIL import Image

@dataclass
class DiagramRequest:
    # Repo

    githubRepoOwner: str = ""
    githubRepoName: str = ""

    # Search Behaviors

    getLanguages: bool = False
    getRequirements: bool = False

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
    canvas: Image = field(default_factory=Image)

    width: int = 0
    height: int = 0

    totalArea: int = 0
    remainingArea: float = 0