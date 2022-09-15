import random
import time

from logger_settings import logger
from settings import data, benchmark
from vk_sender import VkRobot


@benchmark
def start_vk_sender(token: str, message: str, all_groups_id: tuple):
    """Sending messages in vk groups"""

    logger.info(f"{'#' * 15}  Start program {'#' * 15}")
    robot = VkRobot(token, message)
    logger.info('Prepare group_id for posting...')

    count_successful = 0
    logger.info(f"Download {len(all_groups_id)} groups")

    for key, group_id in enumerate(all_groups_id):
        result = robot.post_message_group(group_id['group_id'], message,
                                          ['photo202903451_457247845, photo202903451_457247850'])

        if 'error' not in result.keys():
            count_successful += 1
            logger.info(f"#{key + 1} Record sent in group: {group_id['url']}")
            if key + 1 != len(all_groups_id):
                time.sleep(random.randint(65, 90))
        else:
            logger.warning(f"#{key + 1} Record don't sent in group: {group_id['url']}"
                           f" reason: {result['error']['error_msg']}")

    logger.info(f"{'#' * 15} Finish, sent {count_successful} records from {len(all_groups_id)} {'#' * 15}")


if __name__ == "__main__":
    start_vk_sender(data.token, data.message, data.all_animals_groups_id)
