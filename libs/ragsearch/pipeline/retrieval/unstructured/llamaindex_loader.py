from llama_index.core import SimpleDirectoryReader, GPTVectorStoreIndex

class LlamaIndexLoader:
    """
    Class to load the LlamaIndex from disk or build it from documents.
    """
    def __init__(self, config):
        """
        Initializes the LlamaIndexLoader with the configuration.
        """
        self.index_path = config.get("index_path")
        self.documents_path = config.get("documents_path", None)
        self.index = None
        self._load_or_build_index()

    def _load_or_build_index(self):
        """
        Loads the index from disk or builds a new index from documents.
        """
        if self.index_path:
            # Load pre-existing index
            try:
                self.index = GPTVectorStoreIndex.load_from_disk(self.index_path)
            except Exception as e:
                raise RuntimeError(f"Failed to load index from {self.index_path}: {e}")
        elif self.documents_path:
            # Build new index from documents
            documents = SimpleDirectoryReader(self.documents_path).load_data()
            self.index = GPTVectorStoreIndex.from_documents(documents)
        else:
            raise ValueError("Either 'index_path' or 'documents_path' must be provided in the config.")

    def query(self, query_text):
        """
        Queries the index with the given text and returns the relevant response.
        """
        if not self.index:
            raise RuntimeError("No index is available to query.")
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_text)
        return response.response  # Assuming response.response contains the relevant text
