# Running with Docker

This is an alternative way to run the app using Docker. It does not replace the Conda setup above.

**Framework:** Flask 3.1.3. The app is served on port **8000**.

Requirements: Docker installed and running. The commands below are for a Linux shell (such as Ubuntu). Windows PowerShell versions of steps 2 and 4 are given after step 5.

1. Clone the repository and move into it:

```git clone https://github.com/dfishwick/hgnc-gene-app.git```

```cd hgnc-gene-app```

2. Download the HGNC dataset into `data/`. The dataset is not included in the image, so that gene data is never out of date:

```wget -O data/hgnc_complete_set.txt https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt```

3. Build the image:

```docker build -t gene-lookup-app .```

4. Run the container:

```docker run --rm -p 8000:8000 -v "$(pwd)/data:/app/data:ro" gene-lookup-app```

5. Open http://localhost:8000 in a web browser. Press `Ctrl+C` in the terminal to stop the container.

The `-v` option shares your local `data/` folder with the container as read-only. As with the Conda setup, `data/` must contain exactly one `.txt` file.

The container uses Flask's built-in development server, which is suitable for local use only.

**Windows (PowerShell):** steps 1, 3 and 5 are the same. Use these commands for steps 2 and 4:

```Invoke-WebRequest -Uri https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt -OutFile data\hgnc_complete_set.txt```

```docker run --rm -p 8000:8000 -v "${PWD}\data:/app/data:ro" gene-lookup-app```
