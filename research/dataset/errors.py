class DatasetFoundationError(Exception):
    """Base exception for Dataset Foundation failures."""
    pass

class DatasetConfigurationError(DatasetFoundationError):
    """Raised when the dataset manifest or partition configuration is invalid."""
    pass

class DatasetReaderError(DatasetFoundationError):
    """Raised when a partition reader encounters malformed data or invalid semantics."""
    pass
