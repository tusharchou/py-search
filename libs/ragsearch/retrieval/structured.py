from abc import ABC, abstractmethod
import duckdb
import sqlite3
from pymongo import MongoClient


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

class DuckDBRetriever(BaseRetriever):
    """
    A class to retrieve data from a DuckDB database.
    """

    def __init__(self, config):
        self.db_path = config.get("db_path", "memory")  # Default to in-memory database
        self.connection = None

    def connect(self):
        """
        Establish a connection to DuckDB
        """
        if not self.connection:
            self.connection = duckdb.connect(database=self.db_path)

    def query(self, query: str):
        """
        Perform a SQL query on DuckDB
        """
        self.connect()
        result = self.connection.execute(query).fetchall()
        return result

    def close(self):
        """
         Close the connection to DuckDB
         """
        if self.connection:
            self.connection.close()
            self.connection = None

class MongoDBRetriever(BaseRetriever):
    """
    A class to retrieve data from a MongoDB database.
    """

    def __init__(self, config):
        self.connection = None
        self.config = config

    def connect(self):
        """
        Establish a connection to MongoDB
        """
        if not self.connection:
            self.connection = MongoClient(self.config.get("uri"))

    def query(self, query: str):
        """
         Perform a query on MongoDB
        """
        self.connect()
        db = self.connection[self.config.get("db")]
        collection = db[self.config.get("collection")]
        result = collection.find(query)
        return list(result)

    def close(self):
        """
         Close the connection to MongoDB
        """
        if self.connection:
            self.connection.close()
            self.connection = None


class SQLiteRetriever(BaseRetriever):
    """
    A class to retrieve data from a SQLite database.
    """

    def __init__(self, config):
        self.db_path = config.get("db_path", ":memory:")
        self.connection = None

    def connect(self):
        """
        Establish a connection to SQLite
        """
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)

    def query(self, query: str):
        """
        Perform a SQL query on SQLite
        """
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def close(self):
        """
        Close the connection to SQLite
        """
        if self.connection:
            self.connection.close()
            self.connection = None

def get_retriever(config):
    """
    Factory to dynamically select the retriever based on config.

    Example usage:
        config = {
            "retrieval_type": "structured",
            "db_type": "duckdb" or "sqlite" or "mongodb",
            "db_path": "path_to_your_duckdb_file.db",
            "uri": "mongodb://localhost:27017/",
        }

    Args:
        config (dict): Configuration dictionary containing retrieval type and database parameters.

    Returns:
        BaseRetriever: An instance of a retriever class based on the configuration.

    Raises:
        ValueError: If the retrieval type or database type is not supported.
    """
    retrieval_type = config.get("retrieval_type")
    if retrieval_type == "structured":
        db_type = config.get("db_type")
        if db_type == "duckdb":
            return DuckDBRetriever(config)
        elif db_type == "sqlite":
            return SQLiteRetriever(config)
        elif db_type == "mongodb":
            return MongoDBRetriever(config)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    else:
        raise ValueError(f"Unsupported retrieval type: {retrieval_type}")
