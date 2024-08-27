import os

import pytest

from hakai_data_repo_tests import utils
import logging

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)    


def pytest_addoption(parser):
    parser.addoption("--dir", default=".", action="store", help="Base directory to run tests from")
    parser.addoption(
        "--config-path",
        action="store",
        default="config.yaml",
        help="Search pattern for files",
    )


@pytest.fixture(scope="session")
def dir(request) -> str:
    dir = request.config.getoption("--dir")
    logger.info(f"Base directory: {dir}")
    return dir


@pytest.fixture(scope="session")
def config_path(request) -> str:
    config_path = request.config.getoption("--config-path")
    logger.info(f"Config path: {config_path}")
    return config_path


@pytest.fixture(scope="session")
def config(config_path) -> dict:
    config = utils.read_data_repo_config(config_path)
    logger.info(f"Configuration: {config}")
    return config


@pytest.fixture(scope="session")
def change_base_dir(dir):
    if dir:
        original_dir = os.getcwd()
        os.chdir(dir)
        logger.info(f"Changed directory to {dir}")
        yield
        os.chdir(original_dir)
        logger.info(f"Changed directory back to {original_dir}")
    else:
        yield


@pytest.fixture(scope="session")
def files(config) -> list:
    files = []
    for file in config["data"]["search_pattern"]:
        files += utils.get_file_list(
            file,
            file_ignore=config["file_ignore"],
            recursive=config["data"]["recursive"],
        )
    return files
