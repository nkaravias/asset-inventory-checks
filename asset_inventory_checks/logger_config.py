import logging

def setup_logger():
    logger = logging.getLogger('asset_inventory_checks')
    logger.setLevel(logging.INFO)  # Or DEBUG for more detailed output

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger

logger = setup_logger()