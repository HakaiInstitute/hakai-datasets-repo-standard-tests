import logging
import os
import sys

import pytest

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main():
    return sys.exit(pytest.main())


if __name__ == "__main__":
    main()
