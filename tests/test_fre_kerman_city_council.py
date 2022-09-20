from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_kerman_city_council import FreKermanCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_kerman.html"),
    url="https://cityofkerman.net/city-council-meeting-agendas-minutes/",
)
spider = FreKermanCityCouncilSpider()

freezer = freeze_time("2022-08-14")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "October 12, 2022"


def test_description():
    assert parsed_items[0]["description"] == ""  # noqa


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 10, 12, 0, 0)


def test_status():
    assert parsed_items[0]["status"] == "tentative"


# def test_location():
#     assert parsed_items[0]["location"] == {
#         "name": "EXPECTED NAME",
#         "address": "EXPECTED ADDRESS"
#     }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://cityofkerman.net/city-council-meeting-agendas-minutes/"
    )


def test_links():
    assert parsed_items[0]["links"] == []
    assert parsed_items[2]["links"] == [
        {
            "name": "Regular Meeting Agenda Packet",
            "href": "https://cityofkerman.net/wp-content/uploads/2022/09/Agenda-Packet-22-09-14.pdf", # noqa
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
