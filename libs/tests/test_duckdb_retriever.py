import pytest
from ..ragsearch.pipeline.retrieval.structured import DuckDBRetriever

def test_duckdb_retriever_query():
    config = {"db_path": ":memory:"}
    retriever = DuckDBRetriever(config)
    retriever.connection.execute("CREATE TABLE test (id INT, name STRING);")
    retriever.connection.execute("INSERT INTO test VALUES (1, 'John');")
    result = retriever.query("SELECT * FROM test;")
    assert result == [(1, 'John')]
    retriever.close()