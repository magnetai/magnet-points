import logging
import os

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    
def get_logger(name: str):
    
    # Ensure the log file exists
    log_path = os.path.join(log_dir, f"{name}.log")
    if not os.path.exists(log_path):
        os.makedirs(log_dir, exist_ok=True)
        with open(log_path, "w") as f:
            f.write("")

    # Get logger
    logger = logging.getLogger(name)
    
    # Check if handlers have already been added to avoid duplication.
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File Handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)-9s %(levelname)-6s %(message)s"))
        
        # Console Handler
        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)-9s %(levelname)-6s %(message)s"))

        # Add handlers
        logger.addHandler(file_handler)
        # logger.addHandler(stream_handler)

    return logger