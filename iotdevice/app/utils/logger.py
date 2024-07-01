import logging
import sys
import settings


def get_logger(name, log_file_name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
    file_handler = logging.FileHandler(settings.LOGS_DIR.joinpath(log_file_name + '.log'))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
