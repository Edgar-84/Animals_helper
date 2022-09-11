import pytest

from settings import data
from vk_sender import VkRobot

test_vk_robot = VkRobot(data.token, data.message)


@pytest.mark.parametrize('group_id, message', [('1', 'Hello'),
                                               ('asf', 'Hello 2'),
                                               ('', 'Message'),
                                               ('path', ''),
                                               ('', '')])
def test_post_message_group_error(group_id, message):
    assert 'error' in test_vk_robot.post_message_group(group_id, message)
