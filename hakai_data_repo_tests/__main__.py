import logging
import sys

import click
import pytest

logger = logging.getLogger(__name__)


@click.command()
@click.option("--dir", default=".", help="Base directory to run tests from")
@click.option("--config-path", default="config.yaml", help="Search pattern for files")
@click.option("--log-level", default="INFO", help="Log level")
@click.option("--junit-xml", help="Create junit-xml style report")
def main(dir=".", config_path="config.yaml", log_level="INFO", junit_xml=None):
    logger.info(f"Running tests with arguments: {dir=}, {config_path=}, {log_level=}")
    response = pytest.main(
        args=[
            "--capture=tee-sys",
            f"--log-cli-level={log_level}",
            "--traceconfig",
            "--pyargs",
            "hakai_data_repo_tests",
            "--dir",
            dir,
            "--config-path",
            config_path,
        ]
        + (["--junit-xml", junit_xml] if junit_xml else []),
    )
    sys.exit(response)


if __name__ == "__main__":
    main()
