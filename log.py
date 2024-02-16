import logging

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler
    if not logger.handlers:
        f_handler = logging.FileHandler('app.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(f_handler)

    return logger
