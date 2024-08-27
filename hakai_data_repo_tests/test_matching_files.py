import logging
import re
from glob import glob
from pathlib import Path

logger = logging.getLogger(__name__)


def test_matching_files_check(config):
    """Check if a list of files match an equivalent list of
    files by replaceing a specific expression by another."""
    matched_files = config.get("matched_files", [])
    if not matched_files:
        logger.debug("No matched files to check")
        return
    missing_matches = []
    logger.info("Checking matched files %s", matched_files)
    for group in matched_files:
        logger.info("Checking group %s", group)
        files = glob(group.get("files"), recursive=group.get("recursive", True))
        assert files, f"No files found for pattern {group.get('files')}"
        matched_files = [
            re.sub(group["pattern"], group["replace"], file) for file in files
        ]
        missing_matches = [
            f"{file} -> {matched_file}"
            for file, matched_file in zip(files, matched_files)
            if not Path(matched_file).exists()
        ]

    assert not missing_matches, f"Missing matched files: {missing_matches}"
