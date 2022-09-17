from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_kings_bos import FreKingsBosSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_kings_bos.html"),
    url="https://www.countyofkings.com/community/calendar-of-events",
)
spider = FreKingsBosSpider()

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
    assert parsed_items[0]["title"] == "Board of Supervisors Regular Meeting"


def test_description():
    assert (
        parsed_items[0]["description"]
        == "Check meeting link for meeting details and agenda"
    )


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 9, 13, 9, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_kings_bos/202209130900/x/board_of_supervisors_regular_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Board of Supervisors Chambers, Kings County Government Center",
        "address": "1400 W. Lacey Boulevard, Hanford, California 93230",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.countyofkings.com/community/calendar-of-events"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.countyofkings.com/Home/Components/Calendar/Event/6607/20",  # noqa
            "title": "Meeting Details",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
