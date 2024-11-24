import pytest
from unittest.mock import patch, MagicMock
from libs.ragsearch.retrieval.unstructured import PDFRetriever, TextRetriever, get_unstructured_retriever

@pytest.fixture
def config_pdf():
    return {
        'retrieval_type': 'unstructured',
        'file_type': 'pdf',
        'file_path': 'test.pdf'
    }

@pytest.fixture
def config_text():
    return {
        'retrieval_type': 'unstructured',
        'file_type': 'text',
        'file_path': 'test.txt'
    }

def test_pdf_retriever_query(config_pdf):
    retriever = PDFRetriever(config_pdf)
    with patch.object(retriever, 'connect') as mock_connect:
        mock_loader = MagicMock()
        mock_loader.load.return_value = [MagicMock(page_content="Test PDF content")]
        with patch.object(retriever, 'loader', mock_loader):
            result = retriever.query("Test query")
            assert result == ["Test PDF content"]

def test_text_retriever_query(config_text):
    retriever = TextRetriever(config_text)
    with patch.object(retriever, 'connect') as mock_connect:
        mock_loader = MagicMock()
        mock_loader.load.return_value = [MagicMock(page_content="Test text content")]
        with patch.object(retriever, 'loader', mock_loader):
            result = retriever.query("Test query")
            assert result == ["Test text content"]

def test_get_unstructured_retriever_pdf(config_pdf):
    retriever = get_unstructured_retriever(config_pdf)
    assert isinstance(retriever, PDFRetriever)

def test_get_unstructured_retriever_text(config_text):
    retriever = get_unstructured_retriever(config_text)
    assert isinstance(retriever, TextRetriever)
