import logging
import os
import re
import unittest
import yaml

from . import utils

logger = logging.getLogger(__name__)

# config = utils.read_data_repo_config()
config = yaml.safe_load("""
    data: 
        search_pattern: ['data/**/*']
        recursive: true
    file_naming_convention: '\\d{4}-\\d{2}-\\d{2}.*'
    fileignore: [
        '**/Changelog.txt',
        '**/Aquafluor',
        '**/Instruments',
        '**/DR1900',
        '**/README.md',        
        '**/survey-template.csv'
    ]
"""
)

class TestFileNameConvention(unittest.TestCase):
    def test_filename_convention(self):
        """Review Hakai File Name Convention"""
        convention_expression = config.get("file_naming_convention")
        if convention_expression is None:
            logger.info("No file naming convention specified")
            return

        # Get data file name
        convention = re.compile(convention_expression)
        files = []
        for pattern in config["data"]["search_pattern"]:
            files += utils.get_file_list(
                pattern,
                file_ignore=config.get("fileignore"),
                recursive=config["data"]["recursive"],
            )

        assert len(files) != 0, "Failed to detect any files in repository"
        bad_files = [
            file for file in files if not convention.fullmatch(os.path.basename(file))
        ]
        for f in bad_files:
            logger.error(f"Failed naming convention: {f}")
        assert (
            len(bad_files) == 0
        ), f"The following files do not follow the GEM nameing convention: {bad_files}"

