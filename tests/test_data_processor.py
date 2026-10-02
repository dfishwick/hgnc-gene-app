from hgnc_gene_app.modules.data_processor import cell_to_list


def test_cell_to_list_blank():
    assert cell_to_list("") == []


def test_cell_to_list_one_value():
    assert cell_to_list("value") == ["value"]


def test_cell_to_list_multiple_values():
    assert cell_to_list("value1|value2|value3") == ["value1", "value2", "value3"]


# Spaces are not stripped from the values, as they may be meaningful in
# some contexts. This test ensures that the function preserves spaces.
def test_cell_to_list_spurious_spaces():
    assert cell_to_list("value1 | value2 | value3") == [
        "value1 ",
        " value2 ",
        " value3",
    ]
