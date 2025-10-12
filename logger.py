import logging
from logging.handlers import RotatingFileHandler
import os

# caminho da pasta de logs
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logger(name: str = "app"):

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # criar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita duplicar mensagens se o logger já tiver handlers

    if logger.hasHandlers:
        return logger
    
    # definir fotmato do log
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Handler para o console

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Handler para o arquivo (com rotação)

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=100_00, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Adiciona os handlers ao logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger