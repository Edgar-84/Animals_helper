import glob
import json

from datetime import datetime, date
import requests
import vk_api

from logger_settings import logger
from settings import data
from pprint import pprint


class VkRobot:
    """Work with this class for authorization in VkApi and
    create client for sending messages in groups with image"""

    def __init__(self, token: str, message: str = None):

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

    def search_groups(self, name_group: str, country_id: int, city_id: int) -> list[dict]:
        """Search groups and append in list"""
        result_group = []
        response = self.session.method('groups.search',
                                       {'q': name_group,
                                        'type': 'group',
                                        'country_id': country_id,
                                        'city_id': city_id})
        logger.info(f"Find {response['count']} records for search name {name_group}")
        for page in response['items']:
            result_group.append({
                'url': 'https://vk.com/' + page['screen_name'],
                'id': page['id'],
                'name': page['name']})

        return result_group

    def check_posts_in_group(self, group_id: int, count: int = 3) -> bool:
        """Check how long ago post was written"""

        response = self.session.method('wall.get',
                                       {'owner_id': '-' + str(group_id),
                                        'count': count})

        try:
            time_post = datetime.fromtimestamp(response['items'][3]['date'])
        except IndexError:
            time_post = datetime.fromtimestamp(response['items'][0]['date'])

        now_time = datetime.now()
        today = date(now_time.year, now_time.month, now_time.day)
        second = date(time_post.year, time_post.month, time_post.day)
        result_time = today - second

        if result_time.days < 30:
            return True

        return False

    def get_active_groups(self, groups: list, record: bool = False) -> list:
        """Filter groups for get active"""

        result = []
        logger.info(f"Filtering {len(groups)}...")

        for group in groups:
            if self.check_posts_in_group(group['id']):
                result.append(group)

        logger.info(f"After filtering get {len(result)} groups")

        if record and len(result):
            dt = datetime.now()
            with open(f'new_lists_group{dt.year}_{dt.month}_{dt.day}_{dt.hour}:{dt.minute}:{dt.second}', 'w') as file:
                for row in result:
                    file.write(f"'{row['url']}'," + "\n")

        return result

    @staticmethod
    def get_filter_list(check_list: list, black_list: dict, show: bool = True) -> list:
        """Delete dublicates and filter check_list
         with items in black_list"""
        
        logger.info(f'Get {len(check_list)} for start')
        check_list = set(check_list)
        check_list = list(check_list)
        logger.info(f"After delete dublicates get {len(check_list)} records")
        result = []

        for url in check_list:
            if black_list.get(url) is None:
                result.append(url)

        logger.info(f'Finish filter, get {len(result)} links')    
        if show:
            pprint(result)

        return result
