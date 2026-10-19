"""Tests for `find_gene` using the 5 gene test file."""

from pathlib import Path

import pytest

from hgnc_gene_app.modules.data_processor import (
    read_genes, build_hgnc_id_as_key, build_symbol_as_key,
)
from hgnc_gene_app.modules.search import find_gene

SAMPLE_FILE = Path(__file__).parent / "fixtures" / "hgnc_test_set.txt"


@pytest.fixture
def lookups():
    """Return the test genes, the ID lookup and the symbol lookup."""
    genes = read_genes(SAMPLE_FILE)
    return genes, build_hgnc_id_as_key(genes), build_symbol_as_key(genes)


def test_find_gene_by_id(lookups):
    """Find a gene by its HGNC ID."""
    genes, by_id, by_symbol = lookups
    assert find_gene("HGNC:7", by_id, by_symbol) == genes[3]


def test_find_gene_by_symbol(lookups):
    """Find a gene by its symbol."""
    genes, by_id, by_symbol = lookups
    assert find_gene("A2M", by_id, by_symbol) == genes[3]


def test_find_gene_lowercase_symbol(lookups):
    """Match a symbol typed in lower case."""
    genes, by_id, by_symbol = lookups
    assert find_gene("a2m", by_id, by_symbol) == genes[3]


def test_find_gene_lowercase_id(lookups):
    """Match an HGNC ID typed in lower case."""
    genes, by_id, by_symbol = lookups
    assert find_gene("hgnc:7", by_id, by_symbol) == genes[3]


def test_find_gene_strips_spaces(lookups):
    """Ignore spaces around the query."""
    genes, by_id, by_symbol = lookups
    assert find_gene("  A2M  ", by_id, by_symbol) == genes[3]


def test_find_gene_symbol_with_hyphen(lookups):
    """Match a hyphenated symbol typed in lower case."""
    genes, by_id, by_symbol = lookups
    assert find_gene("a1bg-as1", by_id, by_symbol) == genes[1]


def test_find_gene_bare_number_not_accepted(lookups):
    """Return None for a number without the HGNC: prefix."""
    _, by_id, by_symbol = lookups
    assert find_gene("7", by_id, by_symbol) is None


def test_find_gene_symbol_not_found(lookups):
    """Return None for a symbol that is not in the data."""
    _, by_id, by_symbol = lookups
    assert find_gene("ABC9", by_id, by_symbol) is None


def test_find_gene_id_not_found(lookups):
    """Return None for an HGNC ID that is not in the data."""
    _, by_id, by_symbol = lookups
    assert find_gene("HGNC:999999", by_id, by_symbol) is None


def test_find_gene_empty_text(lookups):
    """Return None for an empty query."""
    _, by_id, by_symbol = lookups
    assert find_gene("", by_id, by_symbol) is None
