"""Tests for the Flask routes using the 5 gene test file.

Page text is passed through `html.unescape` before it is checked, because
the template escapes characters such as apostrophes.
"""

from pathlib import Path
import pytest
import html
from hgnc_gene_app.main import create_app

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def client():
    """Return a test client for an app built from the test data."""
    app = create_app(FIXTURES)
    return app.test_client()


# Homepage
def test_home_page_loads(client):
    """Return the search page with status 200."""
    response = client.get("/")
    assert response.status_code == 200


# Search finds a gene
def test_search_by_symbol_shows_gene_upper_case(client):
    """Show the gene's details when searching by upper case symbol."""
    response = client.post("/search", data={"query": "AKT2"})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "HGNC ID: HGNC:392" in page
    assert "Gene symbol: AKT2" in page
    assert "Gene name: AKT serine/threonine kinase 2" in page
    assert "Aliases: PKBβ" in page
    assert "Previous symbols: none recorded" in page
    assert (
        "Previous names: v-akt murine thymoma viral oncogene homolog 2" in page
    )
    assert "Mane select transcripts: ENST00000392038.7, NM_001626.6" in page


def test_search_by_hgnc_id_shows_gene_upper_case(client):
    """Show the gene's details when searching by HGNC ID."""
    response = client.post("/search", data={"query": "HGNC:392"})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "HGNC ID: HGNC:392" in page
    assert "Gene symbol: AKT2" in page
    assert "Gene name: AKT serine/threonine kinase 2" in page
    assert "Aliases: PKBβ" in page
    assert "Previous symbols: none recorded" in page
    assert (
        "Previous names: v-akt murine thymoma viral oncogene homolog 2" in page
    )
    assert "Mane select transcripts: ENST00000392038.7, NM_001626.6" in page


def test_search_by_symbol_shows_gene_lower_case(client):
    """Show the gene's details when the symbol is typed in lower case."""
    response = client.post("/search", data={"query": "akt2"})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "HGNC ID: HGNC:392" in page
    assert "Gene symbol: AKT2" in page
    assert "Gene name: AKT serine/threonine kinase 2" in page
    assert "Aliases: PKBβ" in page
    assert "Previous symbols: none recorded" in page
    assert (
        "Previous names: v-akt murine thymoma viral oncogene homolog 2" in page
    )
    assert "Mane select transcripts: ENST00000392038.7, NM_001626.6" in page


def test_search_by_hgnc_id_shows_gene_lower_case(client):
    """Show the gene's details when the HGNC ID is typed in lower case."""
    response = client.post("/search", data={"query": "hgnc:392"})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "HGNC ID: HGNC:392" in page
    assert "Gene symbol: AKT2" in page
    assert "Gene name: AKT serine/threonine kinase 2" in page
    assert "Aliases: PKBβ" in page
    assert "Previous symbols: none recorded" in page
    assert (
        "Previous names: v-akt murine thymoma viral oncogene homolog 2" in page
    )
    assert "Mane select transcripts: ENST00000392038.7, NM_001626.6" in page


def test_search_by_hgnc_id_leading_trailing_space_shows_gene(client):
    """Show the gene's details when the query has spaces around it."""
    response = client.post("/search", data={"query": " hgnc:392 "})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "HGNC ID: HGNC:392" in page
    assert "Gene symbol: AKT2" in page
    assert "Gene name: AKT serine/threonine kinase 2" in page
    assert "Aliases: PKBβ" in page
    assert "Previous symbols: none recorded" in page
    assert (
        "Previous names: v-akt murine thymoma viral oncogene homolog 2" in page
    )
    assert "Mane select transcripts: ENST00000392038.7, NM_001626.6" in page


# Search finds nothing
def test_search_by_spurious_append_shows_no_data(client):
    """Show a not found message for an HGNC ID with extra digits added.

    HGNC:392 with 19999 added is not another gene's ID, so this checks that
    the search does not match on a prefix.
    """
    response = client.post("/search", data={"query": "hgnc:39219999"})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "No gene data found for 'hgnc:39219999'" in page


def test_search_by_spurious_input_shows_no_data(client):
    """Show a not found message for a symbol that is not in the data."""
    response = client.post("/search", data={"query": "zzz"})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "No gene data found for 'zzz'" in page


def test_search_by_space_shows_no_input(client):
    """Show a no-input error when the query is only a space."""
    response = client.post("/search", data={"query": " "})
    page = html.unescape(response.get_data(as_text=True))
    assert response.status_code == 200
    assert "Error: No input provided" in page


# Startup error
def test_create_app_no_data_file_raises(tmp_path):
    """Raise FileNotFoundError when the data folder has no .txt file."""
    with pytest.raises(FileNotFoundError):
        create_app(tmp_path)
