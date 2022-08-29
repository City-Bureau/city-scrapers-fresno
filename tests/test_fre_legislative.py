import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from freezegun import freeze_time

from city_scrapers.spiders.fre_legislative import FreLegislativeSpider

freezer = freeze_time("2022-08-28")
freezer.start()

with open(
    join(dirname(__file__), "files", "fre_legislative.json"), "r", encoding="utf-8"
) as f:
    test_response = json.load(f)

spider = FreLegislativeSpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

freezer.stop()

"""
def test_tests():
    print("Please write some tests for this spider or at least disable this one.")
    assert False

Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"] == "Bicycle and Pedestrian Advisory Committee"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 24, 17, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_legislative/202208241730/x/bicycle_and_pedestrian_advisory_committee"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "In Person and/or Electronic Electronic Meeting",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://fresno.legistar.com/DepartmentDetail.aspx?ID=35667&GUID=E23EE8C2-67E6-4528-93BA-15B2290EE616"  # noqa
    )


# def test_links():
# assert parsed_items[0]["links"] == [{
# "href": "EXPECTED HREF",
# "title": "EXPECTED TITLE"
# }]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
