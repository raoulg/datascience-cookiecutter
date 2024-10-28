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
├── data/
│   ├── processed
│   ├── raw
├── dev/
|    ├── notebooks
│    └── scripts
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── main.py
├── references/
├── Makefile
├── README.md
├── pyproject.toml
"""

MAKEFILE_TEMPLATE = """
.PHONY: install test lint format

install:
\trye sync

test:
\tpytest

lint:
\truff check src --fix
\tpyright src

format:
\tisort src
\trye fmt
"""

PYPROJECT_TEMPLATE = """
[project]
name = "{{name}}"
version = "0.1.0"
description = ""
authors = [
\t{name = "{{author}}", email = "{{email}}"},
]
dependencies = [
]
requires-python = ">=3.11"
readme = "README.md"
license = {text = "MIT"}

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{{name}}"]
"""

PYTHONFILES = [
    FileTemplate(filename="__init__.py", content=""),
    FileTemplate(filename="main.py", content="def hi():\n\tprint('hello!')"),
]

DEFAULTTEMPLATE = Folder(
    name="${name}",
    subfolders=[
        Folder(name="${src}", files=PYTHONFILES),
        Folder(
            name="dev",
            subfolders=[
                Folder(
                    name="scripts", files=[FileTemplate(filename="dev.py", content="")]
                ),
                Folder(name="notebooks"),
            ],
        ),
        Folder(
            name="data",
            subfolders=[
                Folder(name="raw"),
                Folder(name="processed"),
            ],
        ),
        Folder(name="references"),
        Folder(name="reports", subfolders=[Folder(name="img")]),
        Folder(name="tests"),
    ],
    files=[
        FileTemplate(filename="Makefile", content=MAKEFILE_TEMPLATE),
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

    @field_validator("configfolder", mode="before")
    def create_configfolder(cls, configfolder: Path) -> Path:
        if not configfolder.exists():
            configfolder.mkdir(parents=True)
            logger.info(f"Created config folder {configfolder}")
        return configfolder
