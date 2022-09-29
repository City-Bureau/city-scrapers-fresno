from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_measure_c_committee import FreMeasureCCommitteeSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_measure_c_committee.html"),
    url="https://measurec.com/meetings/",
)
spider = FreMeasureCCommitteeSpider()

freezer = freeze_time("2022-09-27")
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
    assert parsed_items[0]["title"] == "Committee Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 1, 19, 9, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_measure_c_committee/202201190900/x/committee_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Fresno Council of Government’s Ash Conference Room",
        "address": "2035 Tulare Street, Suite 201, 2nd Floor, Fresno, California",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://measurec.com/meetings/"


# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
