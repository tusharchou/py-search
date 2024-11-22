import pytest

from ..ragsearch.pipeline.retrieval import get_retriever
from ..ragsearch.pipeline.retrieval.duckdb_retriever import DuckDBRetriever


def test_get_retriever_with_valid_config():
    config = {
        "retriever_type": "duckdb",
        "db_path": "test.db"
    }
    retriever = get_retriever(config)
    assert isinstance(retriever, DuckDBRetriever)


def test_get_retriever_with_invalid_config():
    config = {
        "retriever_type": "unknown_type",
    }
    with pytest.raises(ValueError):
        get_retriever(config)


def test_get_retriever_with_missing_config_type():
    config = {
        "db_path": "test.db",
    }
    with pytest.raises(ValueError):
        get_retriever(config)


def test_get_retriever_with_partial_config():
    config = {
        "retriever_type": "duckdb",
    }
    with pytest.raises(KeyError):
        get_retriever(config)
