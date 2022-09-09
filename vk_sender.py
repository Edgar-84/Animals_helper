import glob
import json
import random
import time

import requests
import vk_api

from logger_settings import logger
from settings import data, benchmark

session = vk_api.VkApi(token=data.token)
api = session.get_api()
uploader = vk_api.VkUpload(session)
message = data.message


def get_url_photo_download(group_id: str) -> str:
    """Get url for download photo"""
    result = session.method('photos.getWallUploadServer', {"group_id": group_id})
    return result['upload_url']


def create_image_object(image_path: str) -> dict:
    return {'photo': ('img.jpg', open(image_path, 'rb'))}


def post_message_group(group_id: int, text: str) -> dict:
    """"attachments": '{photo}{202903451}_{457247845}, photo202903451_457247850'
    type, owner_id, media_id"""

    params = {'access_token': data.token,
              "message": text,
              "owner_id": '-' + group_id,
              "attachments": 'photo202903451_457247845, photo202903451_457247850',
              "v": '5.131',
              }

    method_url = 'https://api.vk.com/method/wall.post?'
    response = requests.post(method_url, params)
    result = json.loads(response.text)

    return result


def get_id_photo(group_id: int, path_photo: str) -> str:
    """Get dict with info about download photo"""

    images = glob.glob(path_photo)
    try:
        photo_list = uploader.photo_wall(photos=images, group_id=group_id)
        attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
    except Exception as e:
        logger.error(f"Don't get id_photo {e}")

    return attachment


def get_id_from_link_group(data_links: list) -> list:
    """Get group_id from his url"""

    result_id = []
    for url in data_links:
        response = session.method('utils.resolveScreenName',
                                  {'screen_name': str(url.split('/')[-1])})
        if len(response) == 0:
            continue
        else:
            result_id.append({'url': url, 'group_id': str(response['object_id'])})

    return result_id


@benchmark
def main(all_groups_id: list):
    logger.info(f"{'#' * 15}  Start posting {'#' * 15}")
    count_successful = 0
    logger.info(f"Download {len(all_groups_id)} groups")
    for key, group_id in enumerate(all_groups_id):
        result = post_message_group(group_id['group_id'], message)

        if 'error' not in result.keys():
            count_successful += 1
            logger.info(f"#{key + 1} Запись опубликована в группе: {group_id['url']}")
            if key + 1 != len(all_groups_id):
                time.sleep(random.randint(65, 90))
        else:
            logger.warning(f"#{key + 1} Запись не опубликовалась в группе: {group_id['url']}"
                           f" по причине: {result['error']['error_msg']}")

    logger.info(f"{'#' * 15} Finish, отправлено {count_successful} записей из {len(all_groups_id)} {'#' * 15}")

# all_groups_id = get_id_from_link_group(data.all_animals_groups)
# main(all_groups_id)
