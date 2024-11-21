from .factory import RetrievalFactory

def get_retriever(config: dict):
    """
    Creates and returns a retriever instance based on the provided configuration.

    Args:
        config (dict): A dictionary containing configuration parameters for the retriever.

    Returns:
        object: An instance of a retriever as defined by the RetrievalFactory.
    """
    return RetrievalFactory.create_retriever(config)
