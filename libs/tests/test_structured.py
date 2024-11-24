import unittest
from unittest.mock import patch
from libs.ragsearch.retrieval.structured import (
DuckDBRetriever,
MongoDBRetriever,
SQLiteRetriever,
get_retriever
)

class TestDuckDBRetriever(unittest.TestCase):

    @patch('libs.ragsearch.retrieval.structured.duckdb.connect')
    def test_connect(self, mock_connect):
        config = {
            "db_path": "test.db"
        }
        retriever = DuckDBRetriever(config)
        retriever.connect()
        mock_connect.assert_called_once_with(database="test.db")

    @patch('libs.ragsearch.retrieval.structured.duckdb.connect')
    def test_query(self, mock_connect):
        config = {
            "db_path": "test.db"
        }
        retriever = DuckDBRetriever(config)
        mock_connection = mock_connect.return_value
        mock_connection.execute.return_value.fetchall.return_value = [("result",)]
        result = retriever.query("SELECT * FROM test")
        self.assertEqual(result, [("result",)])
        mock_connection.execute.assert_called_once_with("SELECT * FROM test")

    @patch('libs.ragsearch.retrieval.structured.duckdb.connect')
    def test_close(self, mock_connect):
        config = {
            "db_path": "test.db"
        }
        retriever = DuckDBRetriever(config)
        retriever.connect()
        retriever.close()
        mock_connect.return_value.close.assert_called_once()

class TestMongoDBRetriever(unittest.TestCase):

    @patch('libs.ragsearch.retrieval.structured.MongoClient')
    def test_connect(self, mock_mongo_client):
        config = {
            "uri": "mongodb://localhost:27017/"
        }
        retriever = MongoDBRetriever(config)
        retriever.connect()
        mock_mongo_client.assert_called_once_with("mongodb://localhost:27017/")

    @patch('libs.ragsearch.retrieval.structured.MongoClient')
    def test_query(self, mock_mongo_client):
        config = {
            "uri": "mongodb://localhost:27017/",
            "db": "test_db",
            "collection": "test_collection"
        }
        retriever = MongoDBRetriever(config)
        mock_connection = mock_mongo_client.return_value
        mock_collection = mock_connection[config["db"]][config["collection"]]
        mock_collection.find.return_value = [{"result": "data"}]
        result = retriever.query({})
        self.assertEqual(result, [{"result": "data"}])
        mock_collection.find.assert_called_once_with({})

    @patch('libs.ragsearch.retrieval.structured.MongoClient')
    def test_close(self, mock_mongo_client):
        config = {"uri": "mongodb://localhost:27017/"}
        retriever = MongoDBRetriever(config)
        retriever.connect()
        retriever.close()
        mock_mongo_client.return_value.close.assert_called_once()

class TestSQLiteRetriever(unittest.TestCase):

    @patch('libs.ragsearch.retrieval.structured.sqlite3.connect')
    def test_connect(self, mock_connect):
        config = {
            "db_path": "test.db"
        }
        retriever = SQLiteRetriever(config)
        retriever.connect()
        mock_connect.assert_called_once_with("test.db")

    @patch('libs.ragsearch.retrieval.structured.sqlite3.connect')
    def test_query(self, mock_connect):
        config = {
            "db_path": "test.db"
        }
        retriever = SQLiteRetriever(config)
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = [("result",)]
        result = retriever.query("SELECT * FROM test")
        self.assertEqual(result, [("result",)])
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test")

    @patch('libs.ragsearch.retrieval.structured.sqlite3.connect')
    def test_close(self, mock_connect):
        config = {
            "db_path": "test.db"
        }
        retriever = SQLiteRetriever(config)
        retriever.connect()
        retriever.close()
        mock_connect.return_value.close.assert_called_once()

class TestGetRetriever(unittest.TestCase):

    def test_get_retriever_duckdb(self):
        config = {
            "retrieval_type": "structured",
            "db_type": "duckdb",
            "db_path": "test.db"
        }
        retriever = get_retriever(config)
        self.assertIsInstance(retriever, DuckDBRetriever)

    def test_get_retriever_sqlite(self):
        config = {
            "retrieval_type": "structured",
            "db_type": "sqlite",
            "db_path": "test.db"
        }
        retriever = get_retriever(config)
        self.assertIsInstance(retriever, SQLiteRetriever)

    def test_get_retriever_mongodb(self):
        config = {
            "retrieval_type": "structured",
            "db_type": "mongodb",
            "uri": "mongodb://localhost:27017/"
        }
        retriever = get_retriever(config)
        self.assertIsInstance(retriever, MongoDBRetriever)

    def test_get_retriever_invalid_db_type(self):
        config = {
            "retrieval_type": "structured",
            "db_type": "invalid"
        }
        with self.assertRaises(ValueError):
            get_retriever(config)

    def test_get_retriever_invalid_retrieval_type(self):
        config = {
            "retrieval_type": "invalid"
        }
        with self.assertRaises(ValueError):
            get_retriever(config)

if __name__ == '__main__':
    unittest.main()