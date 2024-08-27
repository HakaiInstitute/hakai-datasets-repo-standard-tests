# hakai-datasets-repo-standard-tests

This repository regroup the standard tests to be applied to the different github data repositories handled by the Hakai Institute.

# How to add to repository

Copy the following yml files to your github repository under the directory `.github/workflows`:

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
          python-version: '3.11'
      - name: Install Hakai Tests
        run: |
          python -m pip install --upgrade pip
          pip install git+https://HakaiInstitute:${{secrets.CI_TOKEN}}@github.com/HakaiInstitute/hakai-datasets-repo-standard-tests.git
      - name: Test with pytest
        run: |
          pytest --pyargs hakai_data_repo_tests
```

## Configuration

The [default configuration](hakai_data_repo_tests/default-config.yaml) used to apply the different tests. In order to modify any aspect of the configuration, copy the [default configuration](hakai_data_repo_tests/default-config.yaml) at the top of you data repository as `config.yaml` and apply the different modifications needed.

##### Ignore files
To ignore a particular list of files from the tests, add the `.fileignore` file at the head of the directory (similar to `.gitignore`) or add the following to the `config.yaml`:

```yaml
ignore_files: [list_of_file_expressions_to_ignore]
```

# Tests applied

### Metadata log tests

1. Review time variables
2. Review latitude and longitude

### Naming convention
