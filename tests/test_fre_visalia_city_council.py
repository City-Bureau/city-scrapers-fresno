import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from freezegun import freeze_time

from city_scrapers.spiders.fre_visalia_city_council import FreVisaliaCityCouncilSpider

freezer = freeze_time("2022-08-29")
freezer.start()

with open(
    join(dirname(__file__), "files", "fre_visalia_city_council.json"),
    "r",
    encoding="utf-8",
) as f:
    test_response = json.load(f)

spider = FreVisaliaCityCouncilSpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

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
    assert parsed_items[0]["start"] == datetime(2022, 9, 6, 19, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"] == "fre_visalia_city_council/202209061900/x/city_council"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "City Council Chambers",
        "address": "707 W. Acequia Ave. Visalia, CA 93292",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://visalia.legistar.com/Calendar.aspx"


"""
def test_links():
    assert parsed_items[0]["links"] == [{
      "href": "",
      "title": ""
    }]
"""


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
