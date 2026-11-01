# Testing

Run tests in the repository root with an active environment.

## Running tests
To run unit and Flask route tests, run the command `pytest`.

Testing uses a small subsample of the HGNC dataset located at `tests/fixtures/hgnc_test_set.txt` (5 genes). 

## Generating a coverage report

To generate a coverage report run the command:

```pytest --cov=hgnc_gene_app --cov-report=term-missing --cov-report=html```

The HTML coverage report can be found in `htmlcov/`. Open `htmlcov/index.html` in a web browser to view the coverage report.

## Continuous integration

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and on pull requests into `main`. On a clean Ubuntu runner it:

1. Builds the Docker image.
2. Downloads the HGNC dataset into `data/`, as the dataset is not stored in the repository.
3. Starts the container and checks that the app responds on port 8000.
4. Runs the tests inside the container with coverage (`pytest --cov=hgnc_gene_app`).
5. Uploads the coverage report to Codecov.

Results are shown by the badges at the top of this README and in the Actions tab on GitHub. The upload step needs a repository secret named `CODECOV_TOKEN`.

CI checks that the image builds and the tests pass. It does not check that the instructions in this README are correct.
