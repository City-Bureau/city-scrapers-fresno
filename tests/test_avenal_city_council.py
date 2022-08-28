from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.avenal_city_council import AvenalCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "avenal_city_council.html"),
    url="https://www.cityofavenal.com/agendacenter",
)
spider = AvenalCityCouncilSpider()

freezer = freeze_time("2022-08-14")
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
    assert (
        parsed_items[0]["title"]
        == "Regular Joint Meeting of the Avenal City Council / Successor Agency/ PFA"
    )


def test_description():
    assert (
        parsed_items[0]["description"]
        == " VIA ZOOM Web Link bit.ly/AvenalCouncil Or by calling +1 669 900 6833 and use meeting ID 872 4344 0488 to join."  # noqa
    )


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 11, 17, 15)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "avenal_city_council/202208111715/x/regular_joint_meeting_of_the_avenal_city_council_successor_agency_pfa"  # noqa
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


# def test_location():
#     assert parsed_items[0]["location"] == {
#         "name": "EXPECTED NAME",
#         "address": "EXPECTED ADDRESS"
#     }


def test_source():
    assert parsed_items[0]["source"] == "https://www.cityofavenal.com/agendacenter"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.cityofavenal.com/AgendaCenter/ViewFile/Agenda/_08112022-385",  # noqa
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
