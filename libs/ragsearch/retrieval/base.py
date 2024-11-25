from abc import ABC, abstractmethod

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

    @abstractmethod
    def close(self):
        """Close the connection or clean up resources."""
        pass
