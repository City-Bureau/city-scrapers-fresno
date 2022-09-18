from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_orange_cove_city_council import (
    FreOrangeCoveCityCouncilSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fre_orange_cove_city_council.html"),
    url="https://cityoforangecove.com/agendas/",
)
spider = FreOrangeCoveCityCouncilSpider()

freezer = freeze_time("2022-09-18")
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
    assert parsed_items[0]["title"] == "PUBLIC WORKSHOP"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 1, 6, 0, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert (
        parsed_items[0]["time_notes"]
        == "Meeting time in unscrapable from this site, please check the meeting agenda link for meeting start time."  # noqa
    )


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_orange_cove_city_council/202201060000/x/public_workshop"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Senior Center",
        "address": "699 6th Street, Orange Cove, California 93646",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://cityoforangecove.com/agendas/"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://cityoforangecove.com/wp-content/uploads/2022/01/JANUARY-6-2022-PUBLIC-WORKSHOP.pdf",  # noqa
            "title": "Meeting Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
