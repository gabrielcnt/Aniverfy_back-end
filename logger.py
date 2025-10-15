import logging
import os
from logging.handlers import RotatingFileHandler


# cria a pasta de logs caso não exista
os.makedirs('logs', exist_ok=True)

def criar_logger(nome_logger='app', nivel=logging.DEBUG):
    logger = logging.getLogger(nome_logger)
    logger.setLevel(nivel)


    # Evita duplicar handlers 
    if not logger.handlers:

        file_handler = RotatingFileHandler(
        'logs/logs.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        mode='a'
        )
        # handler para arquivo
        file_handler = logging.FileHandler('logs/logs.log', mode='a')
        file_handler.setLevel(logging.DEBUG)

        # handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # formato do log
        formato = logging.Formatter('%(levelname)s | %(asctime)s | %(name)s | %(message)s')
        file_handler.setFormatter(formato)
        console_handler.setFormatter(formato)

        # adiciona o formato ao log
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
