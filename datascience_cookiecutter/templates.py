from enum import Enum
from pathlib import Path
from typing import List

from loguru import logger
from pydantic import BaseModel, Field, field_validator


class Languages(Enum):
    PYTHON = "python"


class ReportTypes(Enum):
    LATEX = "tex"
    MARKDOWN = "md"
    PPTX = "pptx"
    QUARTO = "qmd"


class FileTemplate(BaseModel):
    """
    Represents a file template.

    Attributes:
        filename (str): The name of the file.
        content (str): The content of the file.
    """

    filename: str
    content: str


class Folder(BaseModel):
    """
    Represents a folder.

    Attributes:
        name (str): The name of the folder.
        subfolders (Optional[List[Folder]]): List of subfolders.
        files (Optional[List[FileTemplate]]): List of files.
    """

    name: str
    subfolders: List["Folder"] = Field(default_factory=list)
    files: List[FileTemplate] = Field(default_factory=list)


README_TEMPLATE = """
.
├── Makefile
├── README.md
├── data
│   ├── final
│   ├── processed
│   ├── raw
│   └── sim
├── dev
|    ├── notebooks
│    └── scripts
├── docs
├── pyproject.toml
├── references
├── reports
│   ├── img
│   └── report.md
├── test
│   ├── __init__.py
│   └── main.py
└── tests
"""

MAKEFILE_TEMPLATE = """
.PHONY: install test lint format

install:
\tpdm install

test:
\tpdm run pytest

lint:
\tpdm run ruff {{name}}
\tpdm run mypy {{name}}

format:
\tpdm run isort -v {{name}}
\tpdm run black {{name}}
"""

PYPROJECT_TEMPLATE = """
[project]
name = "{{name}}"
version = "0.1.0"
description = ""
authors = [
\t{name = "", email = ""},
]
dependencies = [
]
requires-python = ">=3.9"
readme = "README.md"
license = {text = "MIT"}

[project.optional-dependencies]
lint = [
\t"ruff>=0.0.278",
\t"black>=23.7.0",
\t"isort>=5.12.0",
\t"mypy>=1.4.1",
]

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
"""

PYTHONFILES = [
    FileTemplate(filename="__init__.py", content=""),
    FileTemplate(filename="main.py", content=""),
]

DEFAULTTEMPLATE = Folder(
    name="{{name}}",
    subfolders=[
        Folder(name="{{src}}", files=PYTHONFILES),
        Folder(
            name="dev",
            subfolders=[
                Folder(
                    name="scripts", files=[FileTemplate(filename="main.py", content="")]
                ),
                Folder(name="notebooks"),
            ],
        ),
        Folder(
            name="data",
            subfolders=[
                Folder(name="raw"),
                Folder(name="processed"),
                Folder(name="sim"),
                Folder(name="final"),
            ],
        ),
        Folder(name="docs"),
        Folder(name="references"),
        Folder(name="reports", subfolders=[Folder(name="img")]),
        Folder(name="tests"),
    ],
    files=[
        FileTemplate(filename="README.md", content=README_TEMPLATE),
        FileTemplate(filename="Makefile", content=MAKEFILE_TEMPLATE),
        FileTemplate(filename="pyproject.toml", content=PYPROJECT_TEMPLATE),
    ],
)


class CookiecutterSettings(BaseModel):
    name: str
    path: Path
    git: bool = True
    template: Folder = DEFAULTTEMPLATE
    lang: Languages = Languages.PYTHON
    report_type: ReportTypes = ReportTypes.MARKDOWN
    force: bool = False
    configfolder: Path = Path.home() / ".config" / "cookiecutter"

    @field_validator("configfolder")
    def create_configfolder(cls, configfolder):
        configfolder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created config folder {configfolder}")
        return configfolder
