
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<!-- [![PyPi version](https://badgen.net/pypi/v/mltrainer/)](https://pypi.org/project/mltrainer/) -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents
- [Motivation](#-motivation)
- [Features](#-features)
- [Installation](#️-installation)
- [Basic Usage](#-basic-usage)
- [Default Template](#-default-template)
- [Customizing Templates](#️-customizing-templates)
- [Makefile](#️-makefile)
- [PDM](#️-pdm)
- [pytest](#-pytest)

# 🍪 Data Science Cookiecutter
The Data Science Cookiecutter 🍪 is an opinionated, yet configurable, Python project that provides a template for organizing and setting up data science projects. It uses the Cookiecutter project structure to create a standardized and reproducible project layout.


## 🎯 Motivation
Data science projects often require a well-structured project layout to ensure reproducibility and collaboration. The Data Science Cookiecutter aims to solve this problem by providing a project template. While it follows certain opinions about project organization, it also allows for easy customization to fit different project needs.

## ✨ Features
- Standardized project structure for data science projects
- Automatic generation of project files and folders
- Customizable templates for different project needs
- Customizable for multiple programming languages (currently, the default template currently only has Python)
- Easy project initialization with just a few command-line arguments

## ⚙️ Installation
The Data Science Cookiecutter is on [pypi](https://pypi.org/project/datascience-cookiecutter/) and can be installed using `pip`, `poetry`, `pdm` or `conda`.

```bash
pdm install datascience-cookiecutter
```

# 🚀 Basic Usage
To create a new data science project using the Data Science Cookiecutter, follow these steps:

1. Open a terminal or command prompt.
2. `cd` to the directory where you want to create the project.
3. Run the following command: `cookiecutter myproject` where `myproject` is the name of your project.
4. profit 🎉

## 📁 Default Template
```markdown
.
├── Makefile         <- Makefile for project automation
├── README.md        <- Project documentation and instructions
├── pyproject.toml   <- Configuration file for dependencies and project metadata
├── data             <- Folder to store data
│   ├── final        <- Folder for final processed data
│   ├── processed    <- Folder for intermediate processed data
│   ├── raw          <- Folder for raw data
│   └── sim          <- Folder for simulated data
├── dev              <- Folder for development-related files
│   ├── notebooks    <- Folder for Jupyter notebooks
│   └── scripts      <- Folder for development scripts
├── docs             <- Folder for project documentation
├── myproject        <- Placeholder folder for the project itself (replaced with your project name)
│   ├── __init__.py  <- Python package initialization file
│   └── main.py      <- Main Python script for the project
├── references       <- Folder for reference materials
├── reports          <- Folder for project reports
│   ├── img          <- Folder for images and visualizations used in reports
│   └── report.md    <- Sample report file (Markdown format)
└── tests            <- Folder for project tests
```

## 🛠️ Customizing Templates
If you want to customize the default template used by `cookiecutter`, you can create a `templates.py` file in your `$HOME/.config/cookiecutter` directory. Follow these steps:

1. Open a text editor and create a new file called `templates.py`.
2. Import the necessary classes `Folder` and `FileTemplate` by adding the following lines to `templates.py`:

```python
from datascience_cookiecutter import Folder, FileTemplate
```

Define your custom template using the Folder and FileTemplate classes. Here's a minimal example:
```python
MYTEMPLATE = Folder(
    name="{{name}}",
    subfolders=[
        Folder(name="src", files=[FileTemplate(filename="main.py", content="print('Hello, world!')")]),
        Folder(name="data"),
        Folder(name="docs"),
    ],
    files=[
        FileTemplate(filename="README.md", content="# My {{name}}"),
    ],
)
```

Occurences of `{{name}}` will be replaced by the project name as provided
with `cookiecutter myprojectname`. To use your custom template, simply run the
cookiecutter command with the `--template` option followed by the name of
your custom template. For example:
```bash
$ cookiecutter myproject --template=MYTEMPLATE
```
Enjoy customizing your templates! ✨🧙‍♂️

## 🛠️ Makefile
A Makefile is a file containing a set of instructions, known as targets, used to automate tasks in software development. It provides a convenient way to define and organize common commands for building, testing, and managing a project.

In the provided Makefile, you have the following targets:

- install: Installs project dependencies using `pdm install`.
- test: Runs project tests with `pytest`
- format: Applies code formatting using `isort` and `black`.
- lint: Performs linting and static type checking using `ruff` and `mypy`

To use the Makefile, open a terminal or command prompt, navigate to your project directory, and run the desired target using the make command followed by the target name. For example:

```bash
make install
```

## ❤️ PDM
[PDM](https://pdm.fming.dev/latest/) is a Python package manager and build tool that provides an alternative to other package managers like pip or Poetry. It aims to simplify and enhance the management of project dependencies, virtual environments, and building distributions. Follow the link to install it. If you dont want to use it, you can customize the template to create your own Makefile and pyproject.toml.

The template (and PDM) follow the [PEP 621](https://peps.python.org/pep-0621/) standard for project metadata to use a pyproject.toml file instead of setup.py. This file contains the project metadata and dependencies. It also allows you to specify details like the Python version and the project entry point.

## 🔬 pytest
Pytest is a Python testing framework that allows you to write simple and scalable tests with a clean and expressive syntax. It provides powerful features like fixtures, test discovery, and test selection.

For more information, you can visit the official pytest website: [pytest.org](https://pytest.org)
