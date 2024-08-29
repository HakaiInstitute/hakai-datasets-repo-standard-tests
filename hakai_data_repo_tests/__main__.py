import logging
import os
import sys
from argparse import ArgumentParser

import pytest

logger = logging.getLogger(__name__)


def main(dir=".", config_path="config.yaml", log_level="INFO", junit_xml=None):
    logger.info(f"Running tests with arguments: {dir=}, {config_path=}, {log_level=}")
    return pytest.main(
        args=[
            "--capture=tee-sys",
            f"--log-cli-level={log_level}",
            "--pyargs",
            "hakai_data_repo_tests",
            "--dir",
            dir,
            "--config-path",
            config_path,
        ]
        + (["--junit-xml", junit_xml] if junit_xml else []),
        plugins=["conftest"],
    )


if __name__ == "__main__":
    # Parse command line arguments
    parser = ArgumentParser(description="Run Hakai Data Repository Tests")
    parser.add_argument(
        "--dir",
        default=".",
        action="store",
        help="Base directory to run tests from",
    )
    parser.add_argument(
        "--config-path",
        action="store",
        default="config.yaml",
        help="Search pattern for files (default: {dir}/config.yaml)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        action="store",
        help="Log level (default: INFO)",
    )
    parser.add_argument(
        "--junit-xml",
        action="store",
        help="Create junit-xml style report",
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    result = main(
        args.dir, args.config_path, log_level=args.log_level, junit_xml=args.junit_xml
    )
    sys.exit(result)
