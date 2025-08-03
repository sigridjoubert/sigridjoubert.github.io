import logging

_logger = None  # Global or module-level variable


def create_logger(name: str, level=logging.INFO) -> logging.Logger:
    """Create a logger with console output and a basic formatter."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:  # Prevent duplicate handlers
        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


def get_logger() -> logging.Logger:
    """Singleton getter for a module-level logger."""
    global _logger
    if _logger is None:
        _logger = create_logger(__name__)
    return _logger
