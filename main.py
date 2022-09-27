from logger_settings import logger
from settings import data, benchmark
from vk_sender import VkRobot, SenderMessageVk


timoshka_cat = VkRobot(token=data.token,
                        message=data.message['timoshka'] + data.hashtags['cats_girl_hashtags'],
                        groups_id=data.all_animals_groups_id,
                        photo=['photo202903451_457247845, photo202903451_457247850'],
                        name='robot_one')

masha_dog = VkRobot(token=data.token,
                        message=data.message['masha'] + data.hashtags['dog_hashtags'],
                        groups_id=data.all_dogs_id,
                        photo=['photo202903451_457247853, photo202903451_457247854, photo202903451_457247855'],
                        name='robot_two')


blacki_dog = VkRobot(token=data.token,
                        message=data.message['blacki'] + data.hashtags['dog_hashtags'],
                        groups_id=data.all_dogs_id,
                        photo=['photo202903451_457247858', 'photo202903451_457247859', 'photo202903451_457247860',
                               'photo202903451_457247861'],
                        name='robot_two')


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


if __name__ == "__main__":
    start_vk_sender([blacki_dog])
