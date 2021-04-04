# Software_Engineering_Project_COMP2913

Meet Thursday 1pm

[Coverage Report](https://comp2913_group_40.gitlab.io/software_engineering_project_comp2913/)

## Linting / Testing
Activate the python virtual environment
`.\venv\Scripts\Activate.ps1` in powershell (assuming virtual envirment in venv folder within project directory)

To run linting run `flake8`

To run unit tests run `pytest`

To run both run `tox`

## Writing tests
All tests should be within the approiate folder within the `Tests` folder

Each view / endpoint should have a test file named `test_***.py` which should inherit from a base test file for each section

Every test should test one part of each view / endpoints functionality
