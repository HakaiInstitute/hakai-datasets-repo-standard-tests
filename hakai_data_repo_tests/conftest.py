import logging
import os
from pathlib import Path

import pytest

from hakai_data_repo_tests import utils

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--dir", default=".", action="store", help="Base directory to run tests from"
    )
    parser.addoption(
        "--config-path",
        action="store",
        default="config.yaml",
        help="Search pattern for files",
    )


@pytest.fixture(scope="session")
def dir(request) -> Path:
    dir = Path(request.config.getoption("--dir") or ".").resolve()
    logger.info(f"Base directory: {dir}")
    # Change to base directory and return back to original directory once tests are done
    original_dir = os.getcwd()
    os.chdir(dir)
    logger.info(f"Changed to base directory: {dir}")
    yield dir
    os.chdir(original_dir)
    logger.info(f"Changed back to original directory: {original_dir}")


@pytest.fixture(scope="session")
def config_path(request, dir) -> Path:
    config_path = Path(
        request.config.getoption("--config-path") or "config.yaml"
    ).resolve()
    logger.info(f"Config path: {config_path}")
    if config_path.exists():
        logger.info(f"Configuration file found: {config_path}")
    return config_path


@pytest.fixture(scope="session")
def config(config_path) -> dict:
    config = utils.read_data_repo_config(config_path)
    logger.info(f"Configuration: {config}")
    return config


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
