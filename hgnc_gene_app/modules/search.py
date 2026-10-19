"""Search function for the app.

Used by the `/search` route in `main.py`.
"""


def find_gene(query, by_id, by_symbol):
    """Find a gene in the lookup dictionaries by HGNC ID or by symbol.

    Strip whitespace from the query and convert it to upper-case before lookup.

    A query starting with "HGNC:" is looked up as an ID.
    Anything else is looked up as a symbol.

    Parameters
    ----------
    query : str
        The HGNC ID (*MUST* be prefixed with "HGNC:") or symbol to search for
    by_id : dict
        Dictionary of genes keyed by HGNC ID
        created with `build_hgnc_id_as_key`
    by_symbol : dict
        Dictionary of genes keyed by symbol
        created with `build_symbol_as_key`

    Returns
    -------
    dict or None
        The gene dictionary if found, otherwise None
    """
    cleaned_query = query.strip().upper()
    if cleaned_query.startswith("HGNC:"):
        return by_id.get(cleaned_query)
    return by_symbol.get(cleaned_query)
