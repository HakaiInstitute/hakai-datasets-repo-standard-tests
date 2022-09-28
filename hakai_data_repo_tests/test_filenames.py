import logging
import unittest
from glob import glob
import re

logger = logging.getLogger(__name__)

file_extensions = [".csv", ".txt", ".MON"]
ignore_files = [
    "./instrument-log.csv",
    "./station-log.csv",
    "./stations-log.csv",
    "./requirements.txt",
]
ignore_file_regex = re.compile()
hakai_name_convention = re.compile(
    r"(?P<station>[^\\\/]+)_(?P<serial_number>\d+)_(?P<retrial_date>\d{8})(_rawdata){0,1}\..{3}$"
)


class TestFileNameConvention(unittest.TestCase):
    def test_hakai_filename_convention(self):

        """Review Hakai File Name Convention"""
        # Get data file name
        files = []
        for extension in file_extensions:
            files += glob(
                f"./**/*{extension}",
                recursive=True,
            )

        assert len(files) != 0, "Failed to detect any files in repository"

        # Ignore files
        files = [file for file in files if file not in ignore_files]

        bad_files = [file for file in files if not hakai_name_convention.search(file)]
        assert (
            bad_files is None
        ), f"The following files do no follow the hakai name convention: {bad_files}"
