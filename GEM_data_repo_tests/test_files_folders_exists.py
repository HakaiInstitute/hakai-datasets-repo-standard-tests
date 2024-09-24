import logging
import os
import re
import unittest
from parameterized import parameterized
import yaml
from glob import glob
from pathlib import Path

from . import utils

logger = logging.getLogger(__name__)


# config = utils.read_data_repo_config()
config = yaml.safe_load("""
    data: 
        search_pattern: [
            'data/*/*_survey_final.csv',
            'data/*/*_survey_raw.jpg',
            'data/*/Aquafluor',
            'data/*/Aquafluor/Changelog.txt',
            'data/*/DR1900',
            'data/*/DR1900/Changelog.txt',
            'data/*/Instruments',
            'data/*/Instruments/Changelog.txt',
            'data/*/Aquafluor/*.csv',
            'data/*/Aquafluor/*.xlsx',
            'data/*/Aquafluor/*.jpg',
            'data/*/Aquafluor/*.txt',
            'data/*/DR1900/*.csv',
            'data/*/DR1900/*.xlsx',
            'data/*/DR1900/*.jpg',
            'data/*/DR1900/*.txt',
            'data/*/Instruments/*.csv',
            'data/*/Instruments/*.xlsx',
            'data/*/Instruments/*.txt'
        ]
        recursive: true
"""
)

class TestFilesFoldersExists(unittest.TestCase):

    @parameterized.expand(config["data"]["search_pattern"])
    def test_files_folders_exists(self, search_path):
        """Check if a list of files match an equivalent list of
        files by replaceing a specific expression by another."""

        missing_paths = []
       
        logger.info("Checking path %s", search_path)

        # search for possible paths that might contain the patters in search_pattern
        prefix, delim, last = search_path.rpartition('*/')
        expanded_paths = list(Path('.').glob(f"{prefix}{delim}"))

        # find exact matches for patters in search_pattern   
        files = glob(search_path, recursive=config["data"].get("recursive", True))

        # itirate over all possible paths and report an error if it is not contained in existing files/folder search
        for ep_postfix in expanded_paths:
            ep = str(ep_postfix)
            if not files or  all(ep not in x for x in files):
                msg = f"'/{last}' missing from '{ep}'"
                logger.error(msg)
                missing_paths.append(msg)

        assert (
            not missing_paths
        ), f"{missing_paths}"
