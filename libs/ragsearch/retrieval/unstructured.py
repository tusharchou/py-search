from abc import ABC, abstractmethod
from langchain.document_loaders import PyPDFLoader, TextLoader

class BaseRetriever(ABC):
    """
    Abstract class for unstructured retrievers
    """
    @abstractmethod
    def query(self, query: str):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def connect(self):
        pass


class PDFRetriever(BaseRetriever):
    """
    A class to retrieve data from PDF documents using LangChain's PDF loader.
    """

    def __init__(self, config):
        self.file_path = config.get("file_path")
        self.loader = None

    def connect(self):
        """
        Load the PDF file using LangChain's PyPDFLoader
        """
        if not self.loader:
            self.loader = PyPDFLoader(self.file_path)

    def query(self, query: str):
        """
        Perform a query on the loaded PDF document
        """
        self.connect()
        documents = self.loader.load()
        # Here you can use any querying mechanism, for now, returning the document contents
        return [doc.page_content for doc in documents]

    def close(self):
        """
        Close the PDF loader (if needed)
        """
        self.loader = None


class TextRetriever(BaseRetriever):
    """
    A class to retrieve data from text files using LangChain's TextLoader.
    """

    def __init__(self, config):
        self.file_path = config.get("file_path")
        self.loader = None

    def connect(self):
        """
        Load the text file using LangChain's TextLoader
        """
        if not self.loader:
            self.loader = TextLoader(self.file_path)

    def query(self, query: str):
        """
        Perform a query on the loaded text document
        """
        self.connect()
        documents = self.loader.load()
        # Here you can use any querying mechanism, for now, returning the document contents
        return [doc.page_content for doc in documents]

    def close(self):
        """
        Close the Text loader (if needed)
        """
        self.loader = None


def get_unstructured_retriever(config):
    """
    Factory to dynamically select the unstructured retriever based on config

    Example usage:
    config = {
                "retrieval_type": "unstructured",
                "file_type": "pdf",
                "file_path": "path_to_your_pdf.pdf"
            }
    """
    retrieval_type = config.get("retrieval_type")
    if retrieval_type == "unstructured":
        if config.get("file_type") == "pdf":
            return PDFRetriever(config)
        elif config.get("file_type") == "text":
            return TextRetriever(config)
        else:
            raise ValueError(f"Unsupported file type: {config.get('file_type')}")
    else:
        raise ValueError(f"Unsupported retrieval type: {retrieval_type}")
