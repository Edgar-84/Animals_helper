from logger_settings import logger
from settings import data, benchmark
from vk_sender import VkRobot, SenderMessageVk


@benchmark
def start_vk_sender():
    """Sending messages in vk groups"""

    logger.info(f"{'#' * 15}  Start program {'#' * 15}")
    # robot_one = VkRobot(token=data.token,
    #                     message=data.message['timoshka'] + data.hashtags['cats_girl_hashtags'],
    #                     groups_id=data.all_animals_groups_id,
    #                     photo=['photo202903451_457247845, photo202903451_457247850'],
    #                     name='robot_one')

    robot_two = VkRobot(token=data.token,
                        message=data.message['masha'] + data.hashtags['dog_hashtags'],
                        groups_id=data.all_dogs_id,
                        photo=['photo202903451_457247853, photo202903451_457247854, photo202903451_457247855'],
                        name='robot_two')

    logger.info('Prepare group_id for posting...')

    # logger.info(f"Download {len(robot_one.groups_id)} groups for robot {robot_one.name}")
    logger.info(f"Download {len(robot_two.groups_id)} groups for robot {robot_two.name}")

    # first = SenderMessageVk(robot_one, len(robot_one.groups_id))
    second = SenderMessageVk(robot_two, len(robot_two.groups_id))
    # first_robot = iter(first)
    second_robot = iter(second)

    while True:
        # result_one, count_successful_one = next(first_robot)
        result_two, count_successful_two = next(second_robot)

        if result_two is None: #and result_one
            break

    # logger.info(f"{'#' * 15} Finish, sent {count_successful_one} records from {len(robot_one.groups_id)} {'#' * 15}")
    logger.info(f"{'#' * 15} Finish, sent {count_successful_two} records from {len(robot_two.groups_id)} {'#' * 15}")


if __name__ == "__main__":
    start_vk_sender()
