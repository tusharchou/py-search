import pytest
from ..ragsearch.pipeline.retrieval import RetrievalFactory

def test_create_retriever_structured():
    config = {"retrieval_type": "structured", "db_path": ":memory:"}
    retriever = RetrievalFactory.create_retriever(config)
    assert retriever is not None

def test_create_retriever_unstructured_langchain():
    config = {"retrieval_type": "unstructured", "retrieval_engine": "langchain", "loader_type": "text", "file_path": "sample.txt"}
    retriever = RetrievalFactory.create_retriever(config)
    assert retriever is not None

def test_create_retriever_unstructured_llamaindex():
    config = {"retrieval_type": "unstructured", "retrieval_engine": "llamaindex"}
    with pytest.raises(ValueError):
        RetrievalFactory.create_retriever(config)

def test_create_retriever_invalid_engine():
    config = {"retrieval_type": "unstructured", "retrieval_engine": "unsupported_engine"}
    with pytest.raises(ValueError):
        RetrievalFactory.create_retriever(config)
