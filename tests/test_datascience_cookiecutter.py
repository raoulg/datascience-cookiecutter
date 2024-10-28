import pytest
from pathlib import Path
from unittest.mock import patch
from tempfile import TemporaryDirectory
from shutil import rmtree
from loguru import logger

from datascience_cookiecutter import Cookiecutter, CookiecutterSettings
from datascience_cookiecutter.templates import Folder, FileTemplate


@pytest.fixture
def template_folder():
    return Folder(
        name="my-project",
        subfolders=[
            Folder(
                name="src", files=[FileTemplate(filename="__init__.py", content="")]
            ),
            Folder(name="tests"),
        ],
        files=[FileTemplate(filename="README.md", content="")],
    )


@pytest.fixture
def cookiecutter_settings(template_folder):
    return CookiecutterSettings(
        name="my_project", path=Path("path/to/project"), template=template_folder
    )


def test_check_path_not_empty(tmp_path):
    # Create a temporary file inside the path
    file_path = tmp_path / "file.txt"
    file_path.touch()

    with pytest.raises(ValueError):
        Cookiecutter.check_path(tmp_path)


def test_check_path_empty(tmp_path):
    Cookiecutter.check_path(tmp_path)


def test_add_folder(tmp_path):
    cookiecutter = Cookiecutter(CookiecutterSettings(name="my_project", path=tmp_path))
    folder = Folder(
        name="my_folder",
        subfolders=[],
        files=[FileTemplate(filename="file.txt", content="")],
    )

    cookiecutter.add_folder(tmp_path, folder)

    assert (tmp_path / "my_folder").is_dir()
    assert (tmp_path / "my_folder" / "file.txt").is_file()


def test_make_folders(tmp_path, template_folder):
    cookiecutter = Cookiecutter(CookiecutterSettings(name="my-project", path=tmp_path))

    cookiecutter.make_folders(tmp_path, template_folder)
    print(list(tmp_path.iterdir()))

    assert (tmp_path / "my-project").is_dir(), f"found {list(tmp_path.iterdir())}"
    assert (
        tmp_path / "my-project" / "src"
    ).is_dir(), f"found {list((tmp_path / 'my-project').iterdir())}"
    assert (tmp_path / "my-project" / "src" / "__init__.py").is_file()
    assert (tmp_path / "my-project" / "tests").is_dir()
    assert (tmp_path / "my-project" / "README.md").is_file()


@patch("subprocess.check_call")
def test_git_add_commit(mock_check_call, tmp_path):
    cookiecutter = Cookiecutter(CookiecutterSettings(name="my_project", path=tmp_path))
    repo_path = str(tmp_path)
    commit_msg = "Initial commit"

    cookiecutter.git_add_commit(repo_path, commit_msg)

    mock_check_call.assert_any_call(["git", "-C", repo_path, "add", "."])
    mock_check_call.assert_any_call(
        ["git", "-C", repo_path, "commit", "-m", commit_msg]
    )


def test_personalize_template():
    template_folder = Folder(
        name="{{name}}",
        subfolders=[
            Folder(
                name="{{src}}", files=[FileTemplate(filename="__init__.py", content="")]
            ),
        ],
        files=[FileTemplate(filename="README.md", content="some content")],
    )
    cookiecutter = Cookiecutter(
        CookiecutterSettings(name="my-project", path=Path("path/to/project"))
    )

    personalized_template = cookiecutter.personalize_template()

    assert personalized_template.name == "my-project"
    assert personalized_template.subfolders[0].name == "my_project"
    # assert personalized_template.files[0].content == "some content"


def test_call_force(tmp_path, template_folder):
    cookiecutter = Cookiecutter(
        CookiecutterSettings(name="my_project", path=tmp_path, force=True)
    )

    cookiecutter()

    assert (tmp_path / "my_project").is_dir()
    assert (
        tmp_path / "my_project" / "my_project"
    ).is_dir(), f"found {list((tmp_path / 'my_project').iterdir())}"
    assert (tmp_path / "my_project" / "my_project" / "__init__.py").is_file()
    assert (tmp_path / "my_project" / "tests").is_dir()
    assert (tmp_path / "my_project" / "README.md").is_file()


def test_call_without_force(tmp_path, template_folder):
    cookiecutter = Cookiecutter(
        CookiecutterSettings(
            name="my_project", path=tmp_path, force=False, template=template_folder
        )
    )

    cookiecutter()

    # remove tmp_path from paths
    paths = [str(path).replace(str(tmp_path), "") for path in list(tmp_path.iterdir())]
    print(paths)

    assert (tmp_path / "my-project").is_dir(), f"found {list(tmp_path.iterdir())}"
    assert (
        tmp_path / "my-project" / "src"
    ).is_dir(), f"found {list((tmp_path / 'my_project').iterdir())}"
    assert (tmp_path / "my-project" / "src" / "__init__.py").is_file()
    assert (tmp_path / "my-project" / "tests").is_dir()
    assert (tmp_path / "my-project" / "README.md").is_file()


def test_call_with_git(tmp_path, template_folder):
    cookiecutter = Cookiecutter(
        CookiecutterSettings(name="my_project", path=tmp_path, git=True)
    )

    with patch("subprocess.check_call") as mock_check_call:
        cookiecutter()

    gitpath = tmp_path / "my_project"

    mock_check_call.assert_any_call(["git", "init", str(gitpath)])


def test_call_without_git(tmp_path, template_folder):
    cookiecutter = Cookiecutter(
        CookiecutterSettings(name="my_project", path=tmp_path, git=False)
    )

    with patch("subprocess.check_call") as mock_check_call:
        cookiecutter()

    mock_check_call.assert_not_called()


def test_call_existing_directory_with_force(tmp_path, template_folder):
    # Create a directory with the same name as the project
    existing_directory = tmp_path / "my_project"
    existing_directory.mkdir()

    cookiecutter = Cookiecutter(
        CookiecutterSettings(name="my_project", path=tmp_path, force=True)
    )

    cookiecutter()

    assert (tmp_path / "my_project").is_dir()
    assert (
        tmp_path / "my_project" / "my_project"
    ).is_dir(), f"found {list((tmp_path / 'my_project').iterdir())}"
    assert (tmp_path / "my_project" / "my_project" / "__init__.py").is_file()
    assert (tmp_path / "my_project" / "tests").is_dir()
    assert (tmp_path / "my_project" / "README.md").is_file()


def test_call_existing_directory_with_existing_files(tmp_path, template_folder):
    # Create a directory with the same name as the project
    existing_directory = tmp_path / "my_project"
    existing_directory.mkdir()

    # Create an existing file inside the directory
    existing_file = existing_directory / "existing_file.txt"
    existing_file.touch()

    cookiecutter = Cookiecutter(
        CookiecutterSettings(name="my_project", path=tmp_path, force=False)
    )

    with pytest.raises(ValueError):
        cookiecutter()


def test_call_existing_directory_with_existing_files_with_force(
    tmp_path, template_folder
):
    # Create a directory with the same name as the project
    existing_directory = tmp_path / "my_project"
    existing_directory.mkdir()

    # Create an existing file inside the directory
    existing_file = existing_directory / "existing_file.txt"
    existing_file.touch()

    cookiecutter = Cookiecutter(
        CookiecutterSettings(name="my_project", path=tmp_path, force=True)
    )

    cookiecutter()

    assert (tmp_path / "my_project").is_dir()
    assert (tmp_path / "my_project" / "my_project").is_dir()
    assert (tmp_path / "my_project" / "my_project" / "__init__.py").is_file()
    assert (tmp_path / "my_project" / "tests").is_dir()
    assert (tmp_path / "my_project" / "README.md").is_file()


def test_call_with_temporary_directory(template_folder):
    cookiecutter_settings = CookiecutterSettings(
        name="my-project", path=Path("path/to/project"), template=template_folder
    )

    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        cookiecutter = Cookiecutter(cookiecutter_settings)
        cookiecutter.settings.path = temp_dir_path

        cookiecutter()

        assert (
            temp_dir_path / "my-project"
        ).is_dir(), f"found {list(temp_dir_path.iterdir())}"
        assert (
            temp_dir_path / "my-project" / "src"
        ).is_dir(), f"found {list((temp_dir_path / 'my-project').iterdir())}"
        assert (
            temp_dir_path / "my-project" / "src" / "__init__.py"
        ).is_file(), f"found {list((temp_dir_path / 'my-project' / 'src').iterdir())}"
        assert (temp_dir_path / "my-project" / "tests").is_dir()
        assert (temp_dir_path / "my-project" / "README.md").is_file()
