from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.san_joaquin_valley_air_pollution import (
    SanJoaquinValleyAirPollutionSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "san_joaquin_valley_air_pollution.html"),
    url="https://www.valleyair.org/Board_meetings/GB/GB_meetings_2022.htm",
)
spider = SanJoaquinValleyAirPollutionSpider()

freezer = freeze_time("2022-08-12")
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
        == "San Joaquin Valley Unified Air Pollution Control District Governing Board"
    )


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 18, 9, 0)


# def test_end():
# assert parsed_items[0]["end"] == datetime(2022, 8, 18, 11, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_san_joaquin_valley_air_pollution/202208180900/x/san_joaquin_valley_unified_air_pollution_control_district_governing_board"  # noqa
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Central Region Office, Governing Board Room",
        "address": "1990 E. Gettysburg Avenue, Fresno, CA",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.valleyair.org/Board_meetings/GB/GB_meetings_2022.htm"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "hrefAgenda": "https://www.valleyair.org/Board_meetings/GB/agenda_minutes/Agenda/2022/August/agenda.pdf",  # noqa
            "hrefMinutes": "",
            "hrefPresentations": "",
            "hrefRecording": "",
            "titleAgenda": "Agenda",
            "titleMinutes": "Minutes",
            "titlePresentations": "Presentations",
            "titleRecording": "Recording",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
