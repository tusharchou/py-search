"""
This module contains the DuckDBRetriever class to retrieve data from a DuckDB database.
"""

import duckdb

class DuckDBRetriever:
    """
    A class to retrieve data from a DuckDB database.

    Attributes:
        conn (duckdb.DuckDBPyConnection): The DuckDB connection object.
    """

    def __init__(self, config):
        """
        Initializes the DuckDBRetriever with a connection to the DuckDB database.

        Parameters:
            db_path (str): The path to the DuckDB database file. Defaults to 'your_database.duckdb'.
        """
        # Connect to DuckDB
        self.db_path = config.get("db_path", ":memory:")
        self.connection = duckdb.connect(self.db_path)

    def query(self, query, params=None):
        """
        Executes an SQL query on the DuckDB database and fetches all results.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to pass with the SQL query. Defaults to None.

        Returns:
            list: A list of tuples containing the query results.
        """
        # Execute SQL query with parameters
        return self.connection.execute(query).fetchall()

    def close(self):
        """
        Closes the connection to the DuckDB database.
        """
        self.connection.close()
