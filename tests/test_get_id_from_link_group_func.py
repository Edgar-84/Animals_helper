import pytest

from vk_sender import get_id_from_link_group


@pytest.mark.parametrize('url, response', [('https://vk.com/animalhelp_belarus', '2356436'),
                                           ('https://vk.com/faunagorodahelp', '3531775'),
                                           ('https://vk.com/zooshans_board', '58599695'),
                                           ('https://vk.com/zoomip_belarus', '173432830'),
                                           ('https://vk.com/pitstoplaguna', '54528339'),
                                           ('https://vk.com/daylapudrug', '35147837'),
                                           ('https://vk.com/public59076676', '59076676')])
def test_get_id_from_link_group_good(url, response):
    assert get_id_from_link_group([url])[0]['group_id'] == response


def test_type_error():
    with pytest.raises(AttributeError):
        assert get_id_from_link_group([1234])[0]['group_id']


@pytest.mark.parametrize('url', ['1234',
                                 '1',
                                 '012987',
                                 '12342134',
                                 '00000'])
def test_invalid_links(url):
    assert get_id_from_link_group([url]) == []

