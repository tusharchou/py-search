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

    def __init__(self, db_path='your_database.duckdb'):
        """
        Initializes the DuckDBRetriever with a connection to the DuckDB database.

        Parameters:
            db_path (str): The path to the DuckDB database file. Defaults to 'your_database.duckdb'.
        """
        # Connect to DuckDB
        self.conn = duckdb.connect(db_path)

    def query_db(self, query, params=None):
        """
        Executes an SQL query on the DuckDB database and fetches all results.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to pass with the SQL query. Defaults to None.

        Returns:
            list: A list of tuples containing the query results.
        """
        # Execute SQL query with parameters
        result = self.conn.execute(query, params).fetchall()
        return result

    def close(self):
        """
        Closes the connection to the DuckDB database.
        """
        # Close connection
        self.conn.close()