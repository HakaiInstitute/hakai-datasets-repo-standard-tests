import logging
import os
from fnmatch import fnmatch
from glob import glob
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# Load default configuration
with open(
    Path(__file__).parent / "default-config.yaml", encoding="UTF-8"
) as file_handle:
    config = yaml.load(file_handle, Loader=yaml.loader.SafeLoader)


def read_data_repo_config(config_path="config.yaml", file_ignore_path=".fileignore"):
    """Get dataset repository configuration"""
    config_path = Path(config_path)
    file_ignore_path = Path(file_ignore_path)
    if config_path.exists():
        logger.info("Loading configuration from %s", config_path)
        with open(config_path, encoding="UTF-8") as file_handle:
            config.update(yaml.load(file_handle, Loader=yaml.loader.SafeLoader))
    else:
        logger.warning(
            "No configuration file found. Using default configuration: %s", config
        )

    if file_ignore_path.exists():
        logger.info("Loading file ignore patterns from %s", file_ignore_path)
        if not config.get("file_ignore"):
            config["file_ignore"] = []
        else:
            logger.info(
                "Append file ignore patterns to existing list from configuration file."
            )
            config["file_ignore"] += file_ignore_path.read_text().splitlines()
    return config


def get_file_list(pattern, file_ignore=None, recursive=False):
    """Get a list of files based on the pattern provided. Search can ignore
    a list of specific patterns and go recursively
    through the different sub directories"""
    filenames = glob(pattern, recursive=recursive)
    for ignore in file_ignore:
        filenames = [file for file in filenames if not fnmatch(file, ignore)]
    return filenames
