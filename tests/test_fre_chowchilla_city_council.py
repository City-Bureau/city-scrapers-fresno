from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_chowchilla_city_council import (
    FreChowchillaCityCouncilSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fre_chowchilla_city_council.html"),
    url="https://www.cityofchowchilla.org/agendacenter",
)
spider = FreChowchillaCityCouncilSpider()

freezer = freeze_time("2022-08-28")
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
    assert parsed_items[0]["start"] == datetime(2022, 8, 23, 19, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_chowchilla_city_council/202208231900/x/city_council_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chambers",
        "address": "Chowchilla City Hall 130 S. Second Street, Chowchilla, CA 93610",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://www.cityofchowchilla.org/agendacenter"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.cityofchowchilla.org/AgendaCenter/ViewFile/Agenda/_08232022-482",  # noqa
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
