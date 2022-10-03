from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_selma_city_council import FreSelmaCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_selma_city_council.html"),
    url="https://www.cityofselma.com/government/city_council/council_meetings___agendas.php",  # noqa
)
spider = FreSelmaCityCouncilSpider()

freezer = freeze_time("2022-09-05")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


"""
def test_tests():
    print("Please write some tests for this spider or at least disable this one.")
    assert False

Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"] == "Regular Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 12, 5, 14, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == None


def test_id():
    assert (
        parsed_items[0]["id"] == "fre_selma_city_council/202212051400/x/regular_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chambers",
        "address": "1710 Tucker Street, Selma, California",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.cityofselma.com/government/city_council/council_meetings___agendas.php"  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "hrefAgenda": "https://cms9files.revize.com/selma/No Agenda",
            "hrefPacket": "https://cms9files.revize.com/selma/No Packet",
            "titleAgenda": "Agenda",
            "titlePacket": "Packet",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
