import logging


def main_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        filename='py_log.log',
        filemode='w',
        format='%(asctime)s; %(name)s; %(levelname)s: %(message)s',
        encoding='utf-8'
    )

    return logging.getLogger(name)
