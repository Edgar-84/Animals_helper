import functools
import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv

from groups_links import all_animals_groups, all_animals_groups_id
from logger_settings import logger


@dataclass
class Data:
    token: str
    message: str
    all_animals_groups: list
    login_instagram: str
    password_instagram: str
    all_animals_groups_id: tuple


def benchmark(func):
    """Get runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = int(end_time - start_time)
        logger.info(f"Finished {func.__name__!r} after this time - "
                    f"{get_time_work(run_time)}")
        return value

    return wrapper_timer


def get_time_work(sec: int):
    hours = sec // 3600
    if hours > 0:
        minute = (sec // 60) - (hours * 60)
    else:
        minute = sec // 60
    seconds = sec % 60

    return f"{hours}:{minute}:{seconds}"


load_dotenv()
token = os.getenv("TOKEN")

message = os.getenv('MESSAGE')

all_animals_groups = all_animals_groups
login_instagram = os.getenv("LOGIN_INSTAGRAM")
password_instagram = os.getenv("PASSWORD_INSTAGRAM")
all_animals_groups_id = all_animals_groups_id

data = Data(token, message, all_animals_groups, login_instagram, password_instagram, all_animals_groups_id)
