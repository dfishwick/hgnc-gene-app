"""Tests for the data processing functions using the 5 gene test file."""

from pathlib import Path
import pytest
from hgnc_gene_app.modules.data_processor import (
    cell_to_list, row_to_gene, find_data_file, read_genes,
    build_hgnc_id_as_key, build_symbol_as_key
    )


SAMPLE_FILE = Path(__file__).parent / "fixtures" / "hgnc_test_set.txt"


# Test cell_to_list
def test_cell_to_list_blank():
    """Return an empty list for an empty cell."""
    assert cell_to_list("") == []


def test_cell_to_list_one_value():
    """Return a one item list for a cell with one value."""
    assert cell_to_list("value") == ["value"]


def test_cell_to_list_multiple_values():
    """Split a cell on the "|" separator into a list of values."""
    assert cell_to_list("value1|value2|value3") == [
        "value1",
        "value2",
        "value3",
    ]


def test_cell_to_list_spaces():
    """Keep the spaces around the "|" separator; do not strip them."""
    # Spaces may be meaningful in some contexts, so they are not stripped.
    assert cell_to_list("value1 | value2 | value3") == [
        "value1 ",
        " value2 ",
        " value3",
    ]


# Test row_to_gene
def test_typical_row_to_gene():
    """Convert a typical row, with several values per cell, into a gene."""
    row = {
        "hgnc_id": "HGNC:12345",
        "symbol": "GENE1",
        "name": "Gene One",
        "prev_symbol": "OLDGENE1|OLDGENE2",
        "prev_name": "Old Gene One|Old Gene Two",
        "alias_symbol": "ALIAS1|ALIAS2",
        "mane_select": "ENST12345678910.1|NX_123456789.1",
    }
    expected_gene = {
        "hgnc_id": "HGNC:12345",
        "gene_symbol": "GENE1",
        "gene_name": "Gene One",
        "previous_symbols": ["OLDGENE1", "OLDGENE2"],
        "previous_names": ["Old Gene One", "Old Gene Two"],
        "aliases": ["ALIAS1", "ALIAS2"],
        "mane_select": ["ENST12345678910.1", "NX_123456789.1"],
    }
    assert row_to_gene(row) == expected_gene


def test_row_to_gene_with_brca2():
    """Convert a real BRCA2 row and ignore the unused locus_type column."""
    row = {
        "hgnc_id": "HGNC:1101",
        "symbol": "BRCA2",
        "name": "BRCA2 DNA repair associated",
        "prev_symbol": "FANCD1|FACD|FANCD",
        "prev_name": (
            "Fanconi anemia,"
            " complementation group D1|breast cancer 2,"
            " early onset|breast cancer 2"
        ),
        "alias_symbol": "FAD|FAD1|BRCC2|XRCC11",
        "mane_select": "ENST00000380152.8|NM_000059.4",
        "locus_type": "gene with protein product",
    }
    expected_gene = {
        "hgnc_id": "HGNC:1101",
        "gene_symbol": "BRCA2",
        "gene_name": "BRCA2 DNA repair associated",
        "previous_symbols": ["FANCD1", "FACD", "FANCD"],
        "previous_names": [
            "Fanconi anemia, complementation group D1",
            "breast cancer 2, early onset",
            "breast cancer 2",
        ],
        "aliases": ["FAD", "FAD1", "BRCC2", "XRCC11"],
        "mane_select": ["ENST00000380152.8", "NM_000059.4"],
    }
    assert row_to_gene(row) == expected_gene


def test_row_to_gene_with_empty_cells():
    """Give empty strings and empty lists when every cell is blank."""
    row = {
        "hgnc_id": "",
        "symbol": "",
        "name": "",
        "prev_symbol": "",
        "prev_name": "",
        "alias_symbol": "",
        "mane_select": "",
    }
    expected_gene = {
        "hgnc_id": "",
        "gene_symbol": "",
        "gene_name": "",
        "previous_symbols": [],
        "previous_names": [],
        "aliases": [],
        "mane_select": [],
    }
    assert row_to_gene(row) == expected_gene


# Test find_data_file
def test_find_data_file_one_txt(tmp_path):
    """Find the one .txt file and ignore other file types."""
    txt_file = tmp_path / "data.txt"
    txt_file.write_text("x")
    readme_file = tmp_path / "README.md"
    readme_file.write_text("x")
    assert find_data_file(tmp_path) == txt_file


def test_find_data_file_no_txt(tmp_path):
    """Raise FileNotFoundError when the folder has no .txt file."""
    readme_file = tmp_path / "README.md"
    readme_file.write_text("x")
    with pytest.raises(FileNotFoundError):
        _ = find_data_file(tmp_path)


def test_find_data_file_multiple_txt(tmp_path):
    """Raise ValueError when the folder has more than one .txt file."""
    txt_file1 = tmp_path / "data1.txt"
    txt_file1.write_text("x")
    txt_file2 = tmp_path / "data2.txt"
    txt_file2.write_text("x")
    with pytest.raises(ValueError):
        find_data_file(tmp_path)


# Test read_genes
def test_read_genes_count_and_order():
    """Read all 5 genes from the test file in file order."""
    genes = read_genes(SAMPLE_FILE)
    symbols = [gene["gene_symbol"] for gene in genes]
    assert len(genes) == 5
    assert symbols == ["A1BG", "A1BG-AS1", "A1CF", "A2M", "AKT2"]


def test_read_genes_greek_alias():
    """Read the lower-case beta in the AKT2 alias correctly.

    This checks that the data file is read as UTF-8.
    AKT2 is the fifth gene in the test file.
    """
    genes = read_genes(SAMPLE_FILE)
    assert genes[4]["aliases"] == ["PKBβ"]


def test_read_genes_multiple_values():
    """Read cells with several values into lists."""
    genes = read_genes(SAMPLE_FILE)
    assert genes[2]["aliases"] == [
        "ACF",
        "ASP",
        "ACF64",
        "ACF65",
        "APOBEC1CF",
    ]
    assert genes[3]["mane_select"] == ["ENST00000318602.12", "NM_000014.6"]


def test_read_genes_blank_cells():
    """Give empty lists for blank cells."""
    genes = read_genes(SAMPLE_FILE)
    assert genes[0]["previous_symbols"] == []
    assert genes[0]["previous_names"] == []
    assert genes[0]["aliases"] == []
    assert genes[1]["mane_select"] == []


def test_read_genes_missing_file(tmp_path):
    """Raise FileNotFoundError when the data file does not exist."""
    with pytest.raises(FileNotFoundError):
        read_genes(tmp_path / "missing.txt")


# Test build_hgnc_id_as_key
def test_build_hgnc_id_as_key_keys():
    """Use the HGNC IDs as the keys in file order."""
    genes = read_genes(SAMPLE_FILE)
    lookup = build_hgnc_id_as_key(genes)
    assert list(lookup) == [
        "HGNC:5", "HGNC:37133", "HGNC:24086", "HGNC:7", "HGNC:392"
    ]


def test_build_hgnc_id_as_key_finds_gene():
    """Look up a gene by its HGNC ID."""
    genes = read_genes(SAMPLE_FILE)
    lookup = build_hgnc_id_as_key(genes)
    assert lookup["HGNC:7"] == genes[3]
    assert lookup["HGNC:7"]["gene_symbol"] == "A2M"


def test_build_hgnc_id_as_key_empty_list():
    """Return an empty dictionary for an empty list."""
    assert build_hgnc_id_as_key([]) == {}


# Test build_symbol_as_key
def test_build_symbol_as_key_keys():
    """Use the symbols as the keys in file order."""
    genes = read_genes(SAMPLE_FILE)
    lookup = build_symbol_as_key(genes)
    assert list(lookup) == ["A1BG", "A1BG-AS1", "A1CF", "A2M", "AKT2"]


def test_build_symbol_as_key_finds_gene():
    """Look up a gene by its symbol."""
    genes = read_genes(SAMPLE_FILE)
    lookup = build_symbol_as_key(genes)
    assert lookup["A2M"] == genes[3]
    assert lookup["A2M"]["hgnc_id"] == "HGNC:7"


def test_build_symbol_as_key_upper_cases_key_keeps_symbol():
    """Upper-case the key but keep the original symbol in the gene."""
    genes = [{"gene_symbol": "C1orf43"}]
    lookup = build_symbol_as_key(genes)
    assert list(lookup) == ["C1ORF43"]
    assert lookup["C1ORF43"]["gene_symbol"] == "C1orf43"
