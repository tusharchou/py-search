import pytest
from unittest.mock import patch, mock_open
from libs.ragsearch.retrieval.unstructured import PDFRetriever, TextRetriever, get_retriever

def raises_value_error_if_file_path_not_provided():
    config = {
        "api_url": "https://api.unstructured.io/extract"
    }
    with pytest.raises(ValueError):
        PDFRetriever(config)

def raises_value_error_if_api_url_not_provided():
    config = {
        "file_path": "dummy.pdf"
    }
    with pytest.raises(ValueError):
        PDFRetriever(config)

def raises_value_error_if_api_key_not_provided():
    config = {
        "file_path": "dummy.pdf",
        "api_url": "https://api.unstructured.io/extract"
    }
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError):
            PDFRetriever(config)

def returns_content_from_pdf():
    config = {
        "file_path": "dummy.pdf",
        "api_url": "https://api.unstructured.io/extract",
        "api_key": "dummy_key"
    }
    with patch('requests.post') as mock_post, patch('builtins.open', mock_open(read_data=b"data")):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"text": "dummy content"}
        retriever = PDFRetriever(config)
        content = retriever.query()
        assert content == "dummy content"

def raises_runtime_error_if_api_request_fails():
    config = {
        "file_path": "dummy.pdf",
        "api_url": "https://api.unstructured.io/extract",
        "api_key": "dummy_key"
    }
    with patch('requests.post') as mock_post, patch('builtins.open', mock_open(read_data=b"data")):
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "error"
        retriever = PDFRetriever(config)
        with pytest.raises(RuntimeError):
            retriever.query()

def returns_filtered_content_from_pdf():
    config = {
        "file_path": "dummy.pdf",
        "api_url": "https://api.unstructured.io/extract",
        "api_key": "dummy_key"
    }
    with patch('requests.post') as mock_post, patch('builtins.open', mock_open(read_data=b"data")):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"text": "line1\nline2\nline3"}
        retriever = PDFRetriever(config)
        content = retriever.query(query="line2")
        assert content == ["line2"]

def raises_value_error_if_text_file_path_not_provided():
    config = {}
    with pytest.raises(ValueError):
        TextRetriever(config)

def returns_content_from_text_file():
    config = {
        "file_path": "dummy.txt"
    }
    with patch('unstructured.partition.text.partition_text', return_value=["line1", "line2", "line3"]), patch('builtins.open', mock_open(read_data="data")):
        retriever = TextRetriever(config)
        content = retriever.query()
        assert content == "line1\nline2\nline3"

def returns_filtered_content_from_text_file():
    config = {
        "file_path": "dummy.txt"
    }
    with patch('unstructured.partition.text.partition_text',
               return_value=["line1", "line2", "line3"]), patch('builtins.open',
                                                                mock_open(read_data="data")):
        retriever = TextRetriever(config)
        content = retriever.query(query="line2")
        assert content == ["line2"]

def raises_value_error_if_unsupported_file_type():
    config = {
        "retrieval_type": "unstructured",
        "file_type": "unsupported"
    }
    with pytest.raises(ValueError):
        get_retriever(config)

def raises_value_error_if_unsupported_retrieval_type():
    config = {"retrieval_type": "unsupported"}
    with pytest.raises(ValueError):
        get_retriever(config)

def returns_pdf_retriever_instance():
    config = {
        "retrieval_type": "unstructured",
        "file_type": "pdf",
        "file_path": "dummy.pdf",
        "api_key": "dummy_key"
    }
    retriever = get_retriever(config)
    assert isinstance(retriever, PDFRetriever)

def returns_text_retriever_instance():
    config = {
        "retrieval_type": "unstructured",
        "file_type": "text",
        "file_path": "dummy.txt"
    }
    retriever = get_retriever(config)
    assert isinstance(retriever, TextRetriever)