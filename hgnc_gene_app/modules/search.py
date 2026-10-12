def find_gene(query, by_id, by_symbol):
    """Find a gene in the HGNC data file by HGNC ID or by symbol.

    Parameters
    ----------
    query : str
        the HGNC ID (*MUST* be prefixed with "HGNC:") or symbol to search for
    by_id : build_hgnc_id_as_key dict
        dictionary of genes keyed by HGNC ID
    by_symbol : build_symbol_as_key dict
        dictionary of genes keyed by symbol

    Returns
    -------
    dict or None
        the gene dictionary if found, otherwise None
    """
    cleaned_query = query.strip().upper()
    if cleaned_query.startswith("HGNC:"):
        return by_id.get(cleaned_query)
    return by_symbol.get(cleaned_query)
