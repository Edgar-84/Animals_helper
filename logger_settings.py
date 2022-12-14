import logging
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent


def log_settings():
    """Settings for logger"""

    dt = datetime.now()
    file_log = logging.FileHandler(f'{BASE_DIR}/Status_logs/{dt.day}_{dt.month:02d}_{str(dt.year)}.log', 'a', 'utf-8')
    console_out = logging.StreamHandler()
    logging.basicConfig(handlers=(file_log, console_out),
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        encoding='utf-8')

    logging.getLogger().setLevel(logging.INFO)
    root_logger = logging.getLogger(__name__)

    return root_logger


logger = log_settings()
