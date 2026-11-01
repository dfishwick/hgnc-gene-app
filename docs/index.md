# Project overview

[![Gene Lookup CI](https://github.com/dfishwick/hgnc-gene-app/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/dfishwick/hgnc-gene-app/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/dfishwick/hgnc-gene-app/graph/badge.svg)](https://codecov.io/gh/dfishwick/hgnc-gene-app)

The HUGO Gene Nomenclature Committee Gene Lookup is a Flask 3.1.3 web app to search gene information from HGNC data.

This app looks up the values of HGNC ID, Gene symbol, Gene name, Previous symbols, Previous names, Aliases and MANE select transcripts when searching by HGNC ID or Gene symbol.

# Usage

 Enter the HGNC ID or Gene Symbol in the search field and click the `Search` button. The page will display appropriate lookup values for that gene if a valid ID or symbol has been entered.

***HGNC IDs must include the `HGNC:` prefix (e.g. HGNC:1234)***

***Searches can be upper or lower case***

# Known limitations

The default `data/` path for HGNC dataset is not covered by a test. A default dataset is not included to avoid the risk of supplying the user with outdated information.

Results do not currently include MANE Plus Clinical transcripts as this is not included in the current HGNC dataset.

Issues and requests for additional features can be raised in the issue tab on GitHub: https://github.com/dfishwick/hgnc-gene-app/issues

# Acknowledgments

App factory, route layout, error logging and stylesheet were adapted from: https://github.com/andrewdevereau/web_framework_project
