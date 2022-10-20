import random

import schedule

from logger_settings import logger
from settings import data, benchmark
from vk_sender import VkRobot, SenderMessageVk


blacki_dog = VkRobot(token=data.token,
                     message=data.message['blacki'] + data.hashtags['dog_hashtags'],
                     groups_id=data.all_dogs_id,
                     photo=['photo202903451_457247858', 'photo202903451_457247859', 'photo202903451_457247860',
                            'photo202903451_457247861'],
                     name='blacki_dog')


small_cat = VkRobot(token=data.token,
                    message=data.message['small_cat'] + data.hashtags['small_cat_hashtags'],
                    groups_id=data.all_animals_groups_id,
                    photo=['photo202903451_457247863', 'photo202903451_457247864', 'photo202903451_457247865',
                           'photo202903451_457247866'],
                    name='small_cat')


aristocratka = VkRobot(token=data.token,
                       message=data.message['aristocratka'] + data.hashtags['cats_girl_hashtags'],
                       groups_id=data.all_animals_groups_id,
                       photo=['photo202903451_457247867', 'photo202903451_457247868', 'photo202903451_457247869',
                              'photo202903451_457247870'],
                       name='aristocratka')


@benchmark
def start_vk_sender(objects: list):
    """Sending messages in vk groups"""

    logger.info(f"{'#' * 15}  Start program {'#' * 15}")
    for animal in objects:

        logger.info(f"Download {len(animal.groups_id)} groups for robot {animal.name}")

        object_for_message = SenderMessageVk(animal, len(animal.groups_id))
        second_robot = iter(object_for_message)

        while True:
            result, count_successful = next(second_robot)
            if result is None:
                break

        logger.info(f"{'#' * 15} Finish, sent {count_successful} records from {len(animal.groups_id)} {'#' * 15}")



def main():
    schedule.every().day.at(f'18:{random.randint(10, 30)}').do(start_vk_sender, [blacki_dog])
    schedule.every().sunday.at(f'19:{random.randint(10, 30)}').do(start_vk_sender, [small_cat])
    schedule.every().monday.at(f'19:{random.randint(10, 30)}').do(start_vk_sender, [aristocratka])
    schedule.every().tuesday.at(f'19:{random.randint(10, 30)}').do(start_vk_sender, [small_cat])
    schedule.every().wednesday.at(f'19:{random.randint(10, 30)}').do(start_vk_sender, [aristocratka])
    schedule.every().thursday.at(f'19:{random.randint(10, 30)}').do(start_vk_sender, [small_cat])
    schedule.every().friday.at(f'19:{random.randint(10, 30)}').do(start_vk_sender, [aristocratka])
    schedule.every().saturday.at(f'19:{random.randint(10, 30)}').do(start_vk_sender, [small_cat])
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()

