import functools
import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv

from groups_links import all_animals_groups, all_animals_groups_id, all_dogs_groups, all_dogs_id, message
from logger_settings import logger


@dataclass
class Data:
    token: str
    token_two: str
    login_instagram: str
    password_instagram: str
    message: dict
    all_animals_groups: list
    all_animals_groups_id: tuple
    all_dogs_groups: list
    all_dogs_id: list
    hashtags: dict


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
token_two = os.getenv("TOKEN_2")

login_instagram = os.getenv("LOGIN_INSTAGRAM")
password_instagram = os.getenv("PASSWORD_INSTAGRAM")

message = message

all_animals_groups = all_animals_groups
all_animals_groups_id = all_animals_groups_id

all_dogs_groups = all_dogs_groups
all_dogs_id = all_dogs_id

hashtags = {
    'cats_girl_hashtags': ' #кошкавдар #кошкавдарминск #кошкабесплатно #вдобрыеруки #непокупай #ищухозяина #ищудом',
    'cats_man_hashtags': ' #котвдар #котвдарминск #котбесплатно #вдобрыеруки #непокупай #ищухозяина #ищудом',
    'small_cats_hashtags': ' #котятавдар #котятавдарминск #котятабесплатно #вдобрыеруки #непокупай #ищухозяина #ищудом',
    'small_cat_hashtags': ' #котеноквдар #котеноквдарминск #котенокбесплатно #вдобрыеруки #непокупай #ищухозяина #ищудом',
    'dog_hashtags': ' #собакавдар #собакавдарминск #собакабесплатно #вдобрыеруки #непокупай #ищухозяина #ищудом',
    'small_dogs_hashtags': ' #щенкивдар #щенкивдарминск #щенкибесплатно #вдобрыеруки #непокупай #ищухозяина #ищудом',
}


data = Data(token, token_two, login_instagram, password_instagram, message, all_animals_groups, all_animals_groups_id,
            all_dogs_groups, all_dogs_id, hashtags)
