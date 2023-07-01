import click
from datascience_cookiecutter import CookiecutterSettings, Cookiecutter
from pathlib import Path


@click.command()
@click.argument("projectname")
def main(projectname: str) -> None:
    # Set the default settings
    settings = CookiecutterSettings(
        name=projectname,
        path=Path("."),
        git=True,
    )

    # Create the cookiecutter instance and execute
    cookiecutter = Cookiecutter(settings)
    cookiecutter()

if __name__ == "__main__":
    main()
