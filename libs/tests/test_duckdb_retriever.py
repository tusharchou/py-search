import pytest
import duckdb
from ..ragsearch.pipeline.retrieval.duckdb_retriever import DuckDBRetriever


@pytest.fixture
def duckdb_retriever():
    db_retriever = DuckDBRetriever(':memory:')
    yield db_retriever
    db_retriever.close()


def test_duckdb_retriever_initialization(duckdb_retriever):
    assert duckdb_retriever.conn is not None


def test_duckdb_retriever_query_execution(duckdb_retriever):
    duckdb_retriever.query_db("CREATE TABLE test (id INTEGER, name VARCHAR)")
    duckdb_retriever.query_db("INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob')")
    result = duckdb_retriever.query_db("SELECT * FROM test")
    assert len(result) == 2
    assert result[0] == (1, 'Alice')
    assert result[1] == (2, 'Bob')


def test_duckdb_retriever_query_with_params(duckdb_retriever):
    duckdb_retriever.query_db("CREATE TABLE test (id INTEGER, name VARCHAR)")
    duckdb_retriever.query_db("INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob')")
    result = duckdb_retriever.query_db("SELECT * FROM test WHERE id = ?", (1,))
    assert len(result) == 1
    assert result[0] == (1, 'Alice')


def test_duckdb_retriever_empty_query_result(duckdb_retriever):
    duckdb_retriever.query_db("CREATE TABLE test (id INTEGER, name VARCHAR)")
    result = duckdb_retriever.query_db("SELECT * FROM test")
    assert len(result) == 0

