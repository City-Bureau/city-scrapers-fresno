from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_san_joaquin_city_council import (
    FreSanJoaquinCityCouncilSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fre_san_joaquin_city_council.html"),
    url="https://www.cityofsanjoaquin.org/government.html",
)
spider = FreSanJoaquinCityCouncilSpider()

freezer = freeze_time("2022-09-28")
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
    assert parsed_items[0]["title"] == "San Joaquin City Council"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 1, 7, 18, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Time is unscrapable from this website, meeting time is assumed to be 6:00PM as noted on the website. Please check the agenda link to confirm meeting time."  # noqa
    )


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_san_joaquin_city_council/202201071800/x/san_joaquin_city_council"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Senior Center",
        "address": "21991 Colorado Avenue, San Joaquin, CA",
    }


def test_source():
    assert (
        parsed_items[0]["source"] == "https://www.cityofsanjoaquin.org/government.html"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.cityofsanjoaquin.org//2022/01/01-11-2022_CCA.pdf",
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
