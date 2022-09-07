import os
import time
import functools

from dotenv import load_dotenv
from dataclasses import dataclass
from logger_settings import logger
from groups_links import all_animals_groups


@dataclass
class Data:
    token: str
    message: str
    all_animals_groups: list


def benchmark(func):
    """Get runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        fin_time = round(run_time, 3)
        logger.info(f"Finished {func.__name__!r} after this time - "
                    f"{int(fin_time // 3600)}:{int(fin_time // 60)}:{int(fin_time % 60)}")
        return value
    return wrapper_timer


load_dotenv()
token = os.getenv("TOKEN")


message = """Снаружи серьезный брутал,а внутри сладкий пирожочек...
        Тигрик реально пластилиновый кот,который хочет обнимашки и вкусно 
        покушать,а не это вот всё. Короче отличный компаньон для прокрастинации.
         Минск. 80291911096 @zooshans_by
        #кошкавдар #кошкавдарминск #кошкабесплатно #вдобрыеруки #непокупай #ищухозяина #ищудом"""

all_animals_groups = all_animals_groups


data = Data(token, message, all_animals_groups)
