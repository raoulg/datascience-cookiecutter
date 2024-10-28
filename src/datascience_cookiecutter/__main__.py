import importlib.util
from pathlib import Path

import click
from loguru import logger

from datascience_cookiecutter import Cookiecutter, CookiecutterSettings


@click.command()
@click.argument("projectname")
# make template an optional argument, if not provided, use the default template
@click.option("--template", default="default")
def create_project(projectname: str, template: str) -> None:
    settings = CookiecutterSettings(
        name=projectname,
        path=Path("."),
        git=True,
    )

    # check if settings.configfolder has a templates.py file
    # and load the specified template
    # if it does not. load the default template
    if settings.configfolder.exists():
        templates_file = settings.configfolder / "templates.py"

        if templates_file.exists() and template != "default":
            # Load the module from templates.py
            spec = importlib.util.spec_from_file_location("templates", templates_file)  # type: ignore
            templates_module = importlib.util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(templates_module)  # type: ignore

            # Check if the template exists in the loaded module
            if template in dir(templates_module):
                logger.info(f"Using template {template}")
                selected_template = getattr(templates_module, template)
                settings.template = selected_template
            else:
                logger.warning(f"Template {template} not found in {templates_file}")
                logger.info(f"found templates: {dir(templates_module)}")
                logger.info("Using default template")
                # selected_template = default_template  # Use default template
        else:
            logger.info("Using default template")
            # selected_template = default_template  # Use default template
    else:
        logger.info("Using default template")
        # selected_template = default_template  # Use default template

    # Create the cookiecutter instance and execute
    cookiecutter = Cookiecutter(settings)
    cookiecutter()
