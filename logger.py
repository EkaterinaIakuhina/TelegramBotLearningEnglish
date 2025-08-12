import logging 

def main_logger():
    logging.basicConfig(
        level = logging.INFO, 
        filename='py_log.log', 
        filemode='w', 
        format='%(asctime)s; %(name)s; %(levelname)s: %(message)s', 
    )

    return logging.getLogger(__name__)


