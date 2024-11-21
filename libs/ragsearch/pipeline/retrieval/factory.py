from duckdb_retriever import DuckDBRetriever

class RetrievalFactory:
    """
    Factory class to create different types of retrievers based on configuration.
    """
    @staticmethod
    def create_retriever(config: dict):
        """
        Creates a retriever based on the given configuration.

        Args:
            config (dict): Configuration dictionary containing the retriever type and specific parameters.

        Returns:
            object: An instance of a retriever class based on the configuration.

        Raises:
            ValueError: If the retriever type specified in the configuration is not supported.
        """
        if config.get("retriever_type") == "duckdb":
            return DuckDBRetriever(config["db_path"])
        else:
            raise ValueError("Unsupported retriever type.")

