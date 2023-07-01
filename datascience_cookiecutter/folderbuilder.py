from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

from .templates import CookiecutterSettings, FileTemplate

if TYPE_CHECKING:
    from .templates import Folder


class Cookiecutter:
    def __init__(self, settings: CookiecutterSettings):
        self.settings = settings

    @staticmethod
    def check_path(path: Path) -> None:
        """
        Check if a given path is empty or not.

        Args:
            path (Path): The path to check.

        Raises:
            ValueError: If the path is not empty.
        """
        if path.exists() and path.is_dir() and list(path.iterdir()):
            logger.error(f"Path {path} is not empty, found {list(path.iterdir())}")
            raise ValueError("Make sure the path is empty or use force=True")

    def make_folders(self, path: Path, template: Folder) -> None:
        """
        Create folders based on the given template.

        Args:
            path (Path): The root path to create folders in.
            template (Folder): The folder structure template.
        """
        logger.info("Creating folders from template")
        self.add_folder(path, template)

    def add_folder(self, path: Path, folder: Folder) -> None:
        """
        create the folder
        add subfolders and files

        Args:
            path (Path): The root path to add the folder to.
            folder (Folder): The folder to add.
        """
        folder_path = path / folder.name

        folder_path.mkdir(parents=True, exist_ok=True)

        for subfolder in folder.subfolders:
            self.add_folder(folder_path, subfolder)

        for file in folder.files:
            with open(folder_path / file.filename, "w") as f:
                f.write(file.content)

        if not folder.files and not folder.subfolders:
            with open(folder_path / ".gitkeep", "w") as f:
                f.write("")

    @staticmethod
    def git_add_commit(repo: str, msg: str) -> None:
        """
        Add all files in a repository and commit them.

        Args:
            repo (str): The path to the repository.
            msg (str): The commit message.
        """
        subprocess.check_call(["git", "-C", repo, "add", "."])
        subprocess.check_call(["git", "-C", repo, "commit", "-m", msg])

    def personalize_template(self) -> Folder:
        template = self.settings.template

        # Add the makefile_template to the files list of the DEFAULT_TEMPLATE
        name = self.settings.name
        template.name = template.name.replace("{{name}}", name)

        for tfile in template.files:
            tfile.content = tfile.content.replace("{{name}}", name)

        rootname = name.replace("-", "_")
        for subfolder in template.subfolders:
            if subfolder.name == "{{src}}":
                subfolder.name = rootname
            if subfolder.name == "reports":
                reportfile = FileTemplate(
                    filename=f"report.{self.settings.report_type.value}", content=""
                )
                subfolder.files.append(reportfile)

        return template

    def __call__(self) -> None:
        """
        Initialize a project with the specified parameters.
        """
        path = self.settings.path
        template = self.personalize_template()
        root = path / template.name

        if not self.settings.force:
            self.check_path(root)

        root.mkdir(exist_ok=self.settings.force)
        logger.info(f"Created {root}")

        self.make_folders(path, template)

        if self.settings.git:
            gitpath = path / template.name
            logger.info(f"Initializing git repository in {gitpath}")
            subprocess.check_call(["git", "init", str(gitpath)])
            self.git_add_commit(str(gitpath), "template folders")
