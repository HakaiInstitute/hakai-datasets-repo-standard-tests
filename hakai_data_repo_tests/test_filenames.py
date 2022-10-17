import logging
import unittest
import re
import os

from . import utils

logger = logging.getLogger(__name__)

config = utils.read_data_repo_config()

class TestFileNameConvention(unittest.TestCase):
    def test_filename_convention(self):
        """Review Hakai File Name Convention"""
        convention_expression = config.get('file_naming_convention')
        if convention_expression is None:
            logger.info("No file naming convention specified")
            return

        # Get data file name
        convention = re.compile(convention_expression)
        files = []
        for pattern in config["data"]["search_pattern"]:
            files += utils.get_file_list(pattern, file_ignore=config["file_ignore"],recursive=config["data"]["recursive"])

        assert len(files) != 0, "Failed to detect any files in repository"
        bad_files = [file for file in files if not convention.fullmatch(os.path.basename(file))]
        assert (
            len(bad_files)==0
        ), f"The following files do no follow the hakai name convention: {bad_files}"
