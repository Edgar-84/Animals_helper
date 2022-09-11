import glob
import json

import requests
import vk_api

from logger_settings import logger


class VkRobot:
    """Work with this class for authorization in VkApi and
    create client for sending messages in groups with image"""

    def __init__(self, token: str, message: str):

        self.__token = token
        self.session = vk_api.VkApi(token=token)
        self.api = self.session.get_api()
        self.uploader = vk_api.VkUpload(self.session)
        self.message = message

    def get_url_photo_download(self, group_id: str) -> str:
        """Get url for download photo"""
        result = self.session.method('photos.getWallUploadServer', {"group_id": group_id})
        return result['upload_url']

    @staticmethod
    def create_image_object(image_path: str) -> dict:
        """Create parameters for upload photo"""
        return {'photo': ('img.jpg', open(image_path, 'rb'))}

    def post_message_group(self, group_id: str, text: str, photos_list: list = None) -> dict:
        """Send post in group with photo or not"""

        if photos_list is None:
            photo_attachments = ''
        else:
            photo_attachments = f"{', '.join(photos_list)}"

        params = {'access_token': self.__token,
                  "message": text,
                  "owner_id": '-' + group_id,
                  "attachments": photo_attachments,
                  "v": '5.131',
                  }

        method_url = 'https://api.vk.com/method/wall.post?'
        response = requests.post(method_url, params)
        result = json.loads(response.text)

        return result

    def get_id_photo(self, group_id: int, path_photo: str) -> str:
        """Get str with info about download photo"""

        images = glob.glob(path_photo)
        try:
            photo_list = self.uploader.photo_wall(photos=images, group_id=group_id)
            attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
        except Exception as e:
            logger.error(f"Don't get id_photo {e}")

        return attachment

    def get_id_from_link_group(self, data_links: list) -> list[dict]:
        """Get group_id from his url"""

        result_id = []
        for url in data_links:
            response = self.session.method('utils.resolveScreenName',
                                           {'screen_name': str(url.split('/')[-1])})
            if len(response) == 0:
                continue
            else:
                result_id.append({'url': url, 'group_id': str(response['object_id'])})

        return result_id
