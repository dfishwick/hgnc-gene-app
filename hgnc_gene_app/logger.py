"""Logging setup for the app."""

import logging

# Set logger to DEBUG level so every level of message is sent to handler.
logger = logging.getLogger("hgnc_gene_app")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Handler set to DEBUG level so every level of message is shown.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# Connect the formatter to the handler
stream_handler.setFormatter(formatter)

# Connect the handler to the logger
logger.addHandler(stream_handler)
