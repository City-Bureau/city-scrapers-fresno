from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_exeter_city_council import FreExeterCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_exeter_city_council.html"),
    url="https://cityofexeter.com/documents/",
)
spider = FreExeterCityCouncilSpider()

freezer = freeze_time("2022-09-29")
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
    assert parsed_items[0]["title"] == "City Council"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 9, 13, 18, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Meeting time is unscrapable from website, meeting time is assumed to be 6:30PM as specified on website. Please check agenda link to verify meeting time."  # noqa
    )


def test_id():
    assert (
        parsed_items[0]["id"] == "fre_exeter_city_council/202209131830/x/city_council"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Exeter City Hall",
        "address": "137 North F Street",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://cityofexeter.com/documents/"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://cityofexeter.com/documents/cc-agenda-september-13-2022/",
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
