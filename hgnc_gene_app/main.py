"""Flask application factory for the HGNC gene lookup app.

`create_app` loads the gene data once and defines the home and search routes.

The app is created inside `create_app`, not when the module is imported,
so that tests can create one with a different data folder.
"""

from flask import Flask, render_template, request
from pathlib import Path

from hgnc_gene_app.modules.data_processor import (
    find_data_file,
    read_genes,
    build_hgnc_id_as_key,
    build_symbol_as_key
    )
from hgnc_gene_app.modules.search import find_gene
from hgnc_gene_app.logger import logger


def create_app(data_folder=None):
    """Create and configure the Flask application.

    Parameters
    ----------
    data_folder : pathlib.Path, optional
        Path to the folder containing gene data.
        If `data_folder` is None, the default `data/` folder
        in the repository root will be used.

    Returns
    -------
    Flask
        Configured Flask application instance.

    Raises
    ------
    FileNotFoundError
        When no .txt file is found (raised by `find_data_file`)
    ValueError
        When multiple .txt files are found (raised by `find_data_file`)
    """
    app: Flask = Flask(__name__)
    logger.info("Initialising Flask application")

    # Load the gene lookups
    if data_folder is None:
        data_folder = Path(__file__).parent.parent/"data"
    try:
        data_file = find_data_file(data_folder)
        logger.info(f"Loading data from {data_file}")
        genes = read_genes(data_file)
        by_id = build_hgnc_id_as_key(genes)
        by_symbol = build_symbol_as_key(genes)
        # Store data inside app config
        app.config["BY_ID"] = by_id
        app.config["BY_SYMBOL"] = by_symbol
    # Log the error and where it happened, then raise it again so the
    # app stops instead of running without the data.
    except Exception:
        logger.exception("Failed to load data")
        raise

    # Routes
    @app.route("/")
    def home():
        """Render the homepage.

        Returns
        -------
        str
            The search page HTML.
        """
        logger.debug("Rendering homepage")
        return render_template("index.html")

    @app.route("/search", methods=["POST"])
    def search():
        """Handle search requests.

        Look up the submitted query and show the gene, or an error message
        if the query is empty or matches no gene.

        Returns
        -------
        str
            Rendered template containing gene data or error messages.
        """
        query = request.form.get("query", "").strip()
        logger.debug(f"Received search request for: {query}")

        # Validate input
        if not query:
            logger.warning("No input provided")
            return render_template(
                "index.html",
                error="Error: No input provided",
                gene=None
                )

        # Look up the gene
        gene = find_gene(query, app.config["BY_ID"], app.config["BY_SYMBOL"])

        if gene is None:
            logger.info(f"No key matching: {query}")
            return render_template("index.html",
                                   error=f"No gene data found for '{query}'",
                                   gene=None)

        logger.info(f"Gene data found for {query}")
        return render_template("index.html", error=None, gene=gene)

    return app
