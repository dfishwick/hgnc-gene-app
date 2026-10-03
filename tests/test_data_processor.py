from hgnc_gene_app.modules.data_processor import cell_to_list, row_to_gene


def test_cell_to_list_blank():
    assert cell_to_list("") == []


def test_cell_to_list_one_value():
    assert cell_to_list("value") == ["value"]


def test_cell_to_list_multiple_values():
    assert cell_to_list("value1|value2|value3") == [
        "value1",
        "value2",
        "value3",
    ]


# Spaces are not stripped from the values, as they may be meaningful in
# some contexts. This test ensures that the function preserves spaces.
def test_cell_to_list_spurious_spaces():
    assert cell_to_list("value1 | value2 | value3") == [
        "value1 ",
        " value2 ",
        " value3",
    ]


def test_typical_row_to_gene():
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


# locus type is an example of a column not included in the
# row_to_gene function, and is included in the test to ensure that it does
# not affect the output.
def test_row_to_gene_with_brca2():
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
