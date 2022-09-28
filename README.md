# hakai-datasets-repo-standard-tests

This repository regroup the standard tests to be applied to the different github data repositories handled by the Hakai Institute.

# How To

Copy the following yml files to your github repository:

```yaml
name: Apply Hakai Tests
on:
  push:
    branches: main

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install Hakai Tests
        run: |
          python -m pip install --upgrade pip
          pip install git+https://HakaiInstitute:${{secrets.CI_TOKEN}}@github.com/HakaiInstitute/hakai-datasets-repo-standard-tests.git
      - name: Test with pytest
        run: |
          pytest --pyargs hakai_data_repo_tests
```
