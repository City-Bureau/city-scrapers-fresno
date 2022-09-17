import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from freezegun import freeze_time

from city_scrapers.spiders.fre_fresno_bos import FreFresnoBosSpider

freezer = freeze_time("2022-09-17")
freezer.start()

with open(
    join(dirname(__file__), "files", "fre_fresno_bos.json"), "r", encoding="utf-8"
) as f:
    test_response = json.load(f)

spider = FreFresnoBosSpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

freezer.stop()

"""
def test_tests():
    print("Please write some tests for this spider or at least disable this one.")
    assert False

Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"] == "Board of Supervisors"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 9, 20, 9, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "fre_fresno_bos/202209200930/x/board_of_supervisors"


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Hall of Records",
        "address": "2281 Tulare St, Fresno, CA 93724",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://fresnocounty.legistar.com/DepartmentDetail.aspx?ID=25588&GUID=3B286DE2-6E51-4F51-B62A-BB1EC76C1336"  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://fresnocounty.legistar.com/View.ashx?M=A&ID=895900&GUID=2D5F732A-410E-455F-8690-F5EC133F4D68",  # noqa
            "title": "Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
