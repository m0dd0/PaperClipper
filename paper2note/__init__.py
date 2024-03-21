import logging

# Setup logging
logger = logging.getLogger("paper2note")
logger.setLevel(level=logging.INFO)
if not logger.handlers:
    formatter = logging.Formatter("[paper2note]: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.propagate = False

from .paper2note import paper2note
