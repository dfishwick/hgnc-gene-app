import csv
from hgnc_gene_app.logger import logger


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
        blank) and `previous_symbols`, `previous_names`,`aliases` and
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


def find_data_file(data_folder):
    """Find the HGNC data file in a folder.

    Parameters
    ----------
    data_folder : pathlib.Path
        the folder to search

    Returns
    -------
    pathlib.Path
        the path to the single .txt file

    Raises
    ------
    FileNotFoundError
        when no .txt file is found
    ValueError
        when multiple .txt files are found
    """
    data_files = list(data_folder.glob("*.txt"))
    if len(data_files) == 0:
        raise FileNotFoundError(f"No .txt file found in {data_folder}")
    elif len(data_files) > 1:
        raise ValueError(
            f"Multiple .txt files found in {data_folder}. "
            "Ensure there is only one .txt file in the folder."
        )
    return data_files[0]


def read_genes(file_path):
    """Read the HGNC data file and return a list of gene dictionaries.

    Parameters
    ----------
    file_path : pathlib.Path
        the path to the .txt file

    Returns
    -------
    list of dict
        a list of gene dictionaries, one for each row in the file
    """

    genes = []
    with open(file_path, newline="", encoding="utf-8") as data_file:
        reader = csv.DictReader(data_file, delimiter="\t")
        for row in reader:
            genes.append(row_to_gene(row))
    logger.info(f"Read {len(genes)} genes from {file_path}")
    return genes


def build_hgnc_id_as_key(all_gene_dicts):
    """Build a dictionary with HGNC IDs as keys.

    Parameters
    ----------
    all_gene_dicts : list of dict
        assembled gene dictionaries created by `read_genes` from the HGNC
        data file rows.

    Returns
    -------
    dict
        a dictionary with HGNC IDs as keys and gene dictionaries as values
    """
    return {gene["hgnc_id"]: gene for gene in all_gene_dicts}


def build_symbol_as_key(all_gene_dicts):
    """Build a dictionary with gene symbols as keys.

    Parameters
    ----------
    all_gene_dicts : list of dict
        assembled gene dictionaries created by `read_genes` from the HGNC
        data file rows.

    Returns
    -------
    dict
        a dictionary with gene symbols in capital letters as keys and gene
        dictionaries as values
    """
    return {gene["gene_symbol"].upper(): gene for gene in all_gene_dicts}
