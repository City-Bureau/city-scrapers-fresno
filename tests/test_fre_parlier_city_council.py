from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_parlier_city_council import FreParlierCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_parlier_city_council.html"),
    url="https://parlier.ca.us/agendas/",
)
spider = FreParlierCityCouncilSpider()

freezer = freeze_time("2022-09-17")
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
    assert parsed_items[0]["title"] == "Special Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 9, 16, 0, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Time is unscrapable from the website, please check the meeting agenda link for start time."  # noqa
    )


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_parlier_city_council/202209160000/x/special_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Parlier City Hall",
        "address": "1100 E. Parlier Avenue. Parlier CA. 93648",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://parlier.ca.us/agendas/"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://parlier.ca.us/wp-content/uploads/2022/09/9.16.2022-SPECIAL-AGENDA.pdf",  # noqa
            "title": "Meeting Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
