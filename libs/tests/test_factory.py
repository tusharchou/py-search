import pytest

from ..ragsearch.pipeline.retrieval.duckdb_retriever import DuckDBRetriever
from ..ragsearch.pipeline.retrieval.factory import RetrievalFactory


def test_create_retriever_duckdb():
    config = {
        "retriever_type": "duckdb",
        "db_path": "test.db"
    }
    retriever = RetrievalFactory.create_retriever(config)
    assert isinstance(retriever, DuckDBRetriever)


def test_create_retriever_unsupported_type():
    config = {
        "retriever_type": "unsupported_db",
        "db_path": "test.db"
    }
    with pytest.raises(ValueError, match="Unsupported retriever type."):
        RetrievalFactory.create_retriever(config)
