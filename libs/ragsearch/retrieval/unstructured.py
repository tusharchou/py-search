from abc import ABC, abstractmethod
from unstructured.partition.text import partition_text
import requests


class BaseRetriever(ABC):
    """
    Abstract class for unstructured data retrievers.
    """

    @abstractmethod
    def connect(self):
        """Establish a connection or load data source."""
        pass

    @abstractmethod
    def query(self, query: str):
        """Perform a query on the data source."""
        pass

class PDFRetriever(BaseRetriever, ABC):
    """
    A class to retrieve text data from PDF files using the Unstructured API.

    Args:
        config (dict): Configuration parameters for the retriever.

        Example usage:
        config = {
            "file_path": "path/to/file.pdf",
            "api_url": "https://api.unstructured.io/extract",
            "api_key": "your-unstructured-api-key"
        }

    Returns:
        PDFRetriever: An instance of the PDFRetriever class.

    Raises:
        ValueError: If file path, API URL, or API key is not provided.
        RuntimeError: If the API request fails.
    """

    def __init__(self, config):
        self.file_path = config.get("file_path")
        self.api_url = config.get("api_url", "https://api.unstructured.io/extract")  # Default API endpoint
        self.api_key = config.get("api_key")

    def query(self, query: str = None):
        """
        Extract and return content from the PDF file using the Unstructured API.
        """
        if not self.file_path or not self.api_url or not self.api_key:
            raise ValueError("File path, API URL, and API key must be provided.")

        with open(self.file_path, "rb") as f:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": f},
            )

        if response.status_code != 200:
            raise RuntimeError(f"API request failed: {response.text}")

        content = response.json().get("text", "")

        if query:
            # Basic query-based filtering
            return [line for line in content.split("\n") if query.lower() in line.lower()]
        return content


class TextRetriever(BaseRetriever, ABC):
    """
    A class to retrieve text data from plain text files using the unstructured package.
    """

    def __init__(self, config):
        self.file_path = config.get("file_path")

    def query(self, query: str = None):
        """
        Extract and return content from the text file.
        Optionally, the query parameter can be used for filtering or searching.
        """
        if not self.file_path:
            raise ValueError("File path must be provided in the config.")

        elements = partition_text(filename=self.file_path)
        content = "\n".join([str(el) for el in elements])

        if query:
            # Basic query-based filtering (improve this logic as needed)
            return [line for line in content.split("\n") if query.lower() in line.lower()]
        return content


def get_retriever(config):
    """
    Factory method to get the appropriate unstructured data retriever.
    """
    retrieval_type = config.get("retrieval_type")
    if retrieval_type == "unstructured":
        file_type = config.get("file_type")
        if file_type == "pdf":
            return PDFRetriever(config)
        elif file_type == "text":
            return TextRetriever(config)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    else:
        raise ValueError(f"Unsupported retrieval type: {retrieval_type}")
