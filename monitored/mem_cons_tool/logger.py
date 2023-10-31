import logging
from .config import settings


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARNING)
file_handler = logging.FileHandler(settings.log_file_name, mode=settings.log_file_mode)
f_format = logging.Formatter("[%(asctime)s] %(levelname)s:\t%(message)s")
file_handler.setFormatter(f_format)
logger.addHandler(file_handler)
