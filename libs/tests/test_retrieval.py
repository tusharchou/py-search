import pytest

from ..ragsearch.pipeline.retrieval import get_retriever
#from ..ragsearch.pipeline.retrieval.duckdb_retriever import DuckDBRetriever


# def test_get_retriever_with_valid_config():
#     config = {
#         "type": "duckdb",
#         "database": "test.db"
#     }
#     retriever = get_retriever(config)
#     assert isinstance(retriever, DuckDBRetriever)


def test_get_retriever_with_invalid_config():
    config = {
        "type": "unknown_type",
    }
    with pytest.raises(ValueError):
        get_retriever(config)


def test_get_retriever_with_missing_config_type():
    config = {
        "database": "test.db"
    }
    with pytest.raises(KeyError):
        get_retriever(config)


# def test_get_retriever_with_partial_config():
#     config = {
#         "type": "duckdb"
#     }
#     retriever = get_retriever(config)
#     assert isinstance(retriever, DuckDBRetriever)
