import logging
import os

# cria a pasta de logs caso não exista
os.makedirs('logs', exist_ok=True)

def criar_logger(nome_logger='app', nivel=logging.DEBUG):
    logger = logging.getLogger(nome_logger)
    logger.setLevel(nivel)


    # Evita duplicar handlers 
    if not logger.handlers:
        # handler para arquivo
        file_handler = logging.FileHandler('logs/logs.log', mode='a')
        file_handler.setLevel(logging.WARNING)

        # handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # formato do log
        formato = logging.Formatter('%(levelname)s | %(asctime)s | %(name)s | %(message)s')
        file_handler.setFormatter(formato)
        console_handler.setFormatter(formato)

        # adiciona o formato ao log
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
