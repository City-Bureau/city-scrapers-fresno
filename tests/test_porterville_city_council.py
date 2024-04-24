from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_porterville_city_council import (
    PortervilleCityCouncilSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "porterville_city_council.html"),
    url="https://www.ci.porterville.ca.us/government/city_council/council_meeting_dates.php",  # noqa
)
spider = PortervilleCityCouncilSpider()

freezer = freeze_time("2022-08-15")
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
    assert parsed_items[0]["title"] == "City Council Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 1, 4, 14, 30)


# def test_end():
# assert parsed_items[0]["end"] == datetime(2022, 1, 4, 16, 30)


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Regular meetings are held on the first and third Tuesdays of the month, starting at 5:30 p.m. for Closed Session, and 6:30 p.m. for the public meeting."  # noqa
    )  # noqa


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_porterville_city_council/202201041430/x/city_council_meeting"
    )  # noqa


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chamber at City Hall",
        "address": "291 North Main Street Porterville, California 93257",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.ci.porterville.ca.us/government/city_council/council_meeting_dates.php"  # noqa
    )  # noqa


def test_links():
    assert parsed_items[0]["links"] == [{"href": "", "title": ""}]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
