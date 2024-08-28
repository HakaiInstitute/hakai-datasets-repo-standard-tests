import pytest
import yaml

from hakai_data_repo_tests.__main__ import main


@pytest.fixture(scope="function")
def config():
    return {
        "file_naming_convention": ".*",
        "data": {"search_pattern": ["*"], "recursive": False},
        "file_ignore": [],
    }


def test_file_ignore_files(config, tmp_path):
    # Add tmp files
    tmp_path.joinpath("file1.txt").touch()
    tmp_path.joinpath("file1.csv").touch()
    tmp_path.joinpath(".fileignore").write_text("file1.csv\nconfig.yaml")

    # set config
    config["file_naming_convention"] = "file1.txt"
    (tmp_path / "config.yaml").write_text(yaml.dump(config))
    result = main(dir=tmp_path)
    assert result == 0
