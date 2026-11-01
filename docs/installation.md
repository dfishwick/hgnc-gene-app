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

# Data

Obtain a working dataset from https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt

Place the .txt dataset in the `data/` folder, located in the repository root. From this file the app creates nested Python dictionaries in memory based on HGNC ID and Gene symbol on startup. The `data/` folder must contain only one `.txt` file. 
 

# Running the application

With an active environment, run the command:

```flask --app hgnc_gene_app.main:create_app run```

The app opens at http://127.0.0.1:5000. This address will also be printed in the terminal and can be opened in a web browser.

**The .txt file must already be present in `data/` - The app will not start and raises a `FileNotFoundError` if the `.txt` is missing.**
