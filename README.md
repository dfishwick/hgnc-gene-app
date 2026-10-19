# Project overview

The HUGO Gene Nomenclature Committee Gene Lookup is a Flask 3.1.3 web app to search gene information from HGNC data.

This app looks up the values of HGNC ID, Gene symbol, Gene name, Previous symbols, Previous names, Aliases and MANE select transcripts when searching by HGNC ID or Gene symbol.


---

# Installation and setup

The project uses Conda to create an environment with a pinned Python version. Ensure Conda and Git are installed before setup.

- Conda: https://docs.conda.io/projects/conda/en/stable/user-guide/install
- Git: https://git-scm.com

To set up a local environment and package install, run the following commands:

1. Clone the repository:

```git clone https://github.com/dfishwick/hgnc-gene-app.git```

```cd hgnc-gene-app```

2. Create the environment:

```conda env create -f environment.yml```

3. Activate the environment:

```conda activate hgnc-gene-app```

4. Install the package:

```pip install -e .```

---

# Data

Obtain a working dataset from https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt

Place the .txt dataset in the `data/` folder, located in the repository root. From this file the app creates nested Python dictionaries in memory based on HGNC ID and Gene symbol on startup. The `data/` folder must contain only one `.txt` file. 
 
---

# Running the application

With an active environment, run the command:

```flask --app hgnc_gene_app.main:create_app run```

The app opens at http://127.0.0.1:5000. This address will also be printed in the terminal and can be opened in a web browser.

**The .txt file must already be present in `data/` - The app will not start and raises a `FileNotFoundError` if the `.txt` is missing.**

---

# Usage

 Enter the HGNC ID or Gene Symbol in the search field and click the `Search` button. The page will display appropriate lookup values for that gene if a valid ID or symbol has been entered.

***HGNC IDs must include the `HGNC:` prefix (e.g. HGNC:1234)***

***Searches can be upper or lower case***

---

# Testing

Run tests in the repository root with an active environment.

## Running tests
To run unit and Flask route tests, run the command `pytest`.

Testing uses a small subsample of the HGNC dataset located at `tests/fixtures/hgnc_test_set.txt` (5 genes). 

## Generating a coverage report

To generate a coverage report run the command:

```pytest --cov=. --cov-report=term-missing --cov-report=html```

The HTML coverage report can be found in `htmlcov/`. Open `htmlcov/index.html` in a web browser to view the coverage report.

---

# Known limitations

The default `data/` path for HGNC dataset is not covered by a test. A default dataset is not included to avoid the risk of supplying the user with outdated information.

Results do not currently include MANE Plus Clinical transcripts as this is not included in the current HGNC dataset.

Issues and requests for additional features can be raised in the issue tab on GitHub: https://github.com/dfishwick/hgnc-gene-app/issues

---

# Acknowledgments

App factory, route layout, error logging and stylesheet were adapted from: https://github.com/andrewdevereau/web_framework_project

