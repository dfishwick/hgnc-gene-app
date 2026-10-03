def cell_to_list(cell_contents):
    """Convert cell contents into a list of strings.

    Parameters
    ----------
    cell_contents : str
        The text in the cell, "|" separated for multiple values.
        Empty cells are represented as "".

    Returns
    -------
    list of str
        A list of strings, or an empty list if the cell is empty.
    """
    if cell_contents == "":
        return []
    return cell_contents.split("|")


def row_to_gene(row):
    """Convert a row of data into a gene dictionary.

    Parameters
    ----------
    row : dict
        A dictionary representing a row of data
        with keys corresponding to column names:
        'hgnc_id', 'symbol', 'name', 'prev_symbol', 'prev_name',
        'alias_symbol', 'mane_select'.
        Other columns are ignored.

    Returns
    -------
    dict
        A dictionary describing one gene, with the keys `hgnc_id`,
        `gene_symbol`, `gene_name` (text, an empty string if the cell is
        blank) and `previous_symbols`, `previous_names` and `aliases`
        `mane_select` (lists of text, an empty list if the cell is blank).
    """
    return {
        "hgnc_id": row["hgnc_id"],
        "gene_symbol": row["symbol"],
        "gene_name": row["name"],
        "previous_symbols": cell_to_list(row["prev_symbol"]),
        "previous_names": cell_to_list(row["prev_name"]),
        "aliases": cell_to_list(row["alias_symbol"]),
        "mane_select": cell_to_list(row["mane_select"]),
    }
