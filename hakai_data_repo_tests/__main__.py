import logging
import os
import sys
from argparse import ArgumentParser

import pytest

logger = logging.getLogger(__name__)


def main(dir, config_path, log_level="INFO"):
    logger.info(f"Running tests with arguments: {args}")
    return sys.exit(
        pytest.main(
            args=[
                "--capture=tee-sys",
                f"--log-cli-level={log_level}",
                "--pyargs",
                "hakai_data_repo_tests",
                f"--dir={dir}",
                f"--config-path={config_path}",
            ]
        )
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
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    main(args.dir, args.config_path, log_level=args.log_level)
