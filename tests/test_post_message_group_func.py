import pytest

from vk_sender import post_message_group


@pytest.mark.parametrize('group_id, message', [('1', 'Hello'),
                                               ('asf', 'Hello 2'),
                                               ('', 'Message'),
                                               ('path', ''),
                                               ('', '')])
def test_post_message_group_error(group_id, message):
    assert 'error' in post_message_group(group_id, message)
