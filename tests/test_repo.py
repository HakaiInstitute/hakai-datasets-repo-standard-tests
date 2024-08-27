import pytest

from hakai_data_repo_tests import test_matching_files


@pytest.fixture(scope="module")
def config():
    return {
        "file_naming_convention": ".*",
        "data": {"search_pattern": ["*"], "recursive": False},
        "file_ignore": [],
    }


@pytest.fixture
def dir():
    return "test_repo"


class TestMatchingFiles:
    def test_sucessfull_matching_file_check(self, config, tmp_path):
        # Add tmp files
        tmp_path.joinpath("file1.txt").touch()
        tmp_path.joinpath("file1.csv").touch()
        # set config
        config = {
            "matched_files": [
                {"files": f"{tmp_path}/*", "pattern": ".txt", "replace": ".csv"}
            ]
        }
        test_matching_files.test_matched_files_check(config)

    def test_fail_matching_file_check(self, config, tmp_path):
        # Add tmp files
        tmp_path.joinpath("file1.txt").touch()
        # set config
        config = {
            "matched_files": [
                {"files": f"{tmp_path}/*", "pattern": ".txt", "replace": ".csv"}
            ]
        }
        with pytest.raises(AssertionError):
            test_matching_files.test_matched_files_check(config)
