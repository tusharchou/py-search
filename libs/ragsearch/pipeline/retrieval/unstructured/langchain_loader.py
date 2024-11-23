from langchain_community.document_loaders import TextLoader


class LangChainLoader:
    """
    Class to load documents for the language chain.
    """
    def __init__(self, config):
        """
        Initializes the LangChainLoader with the configuration.
        """
        loader_type = config.get("loader_type", "text")
        if loader_type == "text":
            self.loader = TextLoader(config["file_path"])
        else:
            raise ValueError(f"Unsupported loader type: {loader_type}")

    def load_documents(self):
        """
        Loads documents from the configured source.
        """
        return self.loader.load()
