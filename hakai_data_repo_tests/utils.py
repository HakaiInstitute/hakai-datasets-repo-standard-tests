import yaml
from fnmatch import fnmatch
from glob import glob
import os

# Load default configuration
with open(
    os.path.join(os.path.dirname(__file__), "default-config.yaml"), encoding="UTF-8"
) as file_handle:
    config = yaml.load(file_handle, Loader=yaml.loader.SafeLoader)


def read_data_repo_config():
    """Get dataset repository configuration"""
    if os.path.exists("config.yaml"):
        with open("config.yaml", encoding="UTF-8") as file_handle:
            config.update(yaml.load(file_handle, Loader=yaml.loader.SafeLoader))

    if os.path.exists(".fileignore"):
        with open(".fileignore", encoding="UTF-8") as file_handle:
            config["file_ignore"] = [line.strip() for line in file_handle.readlines()]
    return config


def get_file_list(pattern, file_ignore=None, recursive=False):
    """Get a list of files based on the pattern provided. Search can ignore
    a list of specific patterns and go recursively
    through the different sub directories"""
    filenames = glob(pattern, recursive=recursive)
    for ignore in file_ignore:
        filenames = [file for file in filenames if not fnmatch(file, ignore)]
    return filenames
