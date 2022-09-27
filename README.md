# hakai-datasets-repo-standard-tests

This repository regroup the standard tests to be applied to the different github data repositories handled by the Hakai Institute.

# How To

Copy the following yml files to your github repository:

```yaml
name: Python package

on:
  commit:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Test with pytest
        run: |
          pytest
```
