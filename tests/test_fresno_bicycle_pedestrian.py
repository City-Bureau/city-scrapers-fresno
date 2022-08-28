from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import ADVISORY_COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fresno_bicycle_pedestrian import (
    FresnoBicyclePedestrianSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fresno_bicycle_pedestrian.html"),
    url="https://fresno.legistar.com/Calendar.aspx",
)
spider = FresnoBicyclePedestrianSpider()

freezer = freeze_time("2022-08-08")
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
    assert parsed_items[0]["title"] == "Bicycle and Pedestrian Advisory Committee"


def test_description():
    assert parsed_items[0]["description"] == " "


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 24, 17, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == " "


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fresno_bicycle_pedestrian/202208241730/x/bicycle_and_pedestrian_advisory_committee" # noqa
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "'In Person and/or Electronic Electronic Meeting'",
    }


def test_source():
    assert parsed_items[0]["source"] == "EXPECTED URL"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "hrefAgenda": "https://fresno.legistar.com/View.ashx?M=A&ID=925233&GUID=F1C9A953-1959-481E-B70D-FCECD8285489", # noqa
            "hrefMeetingDetails": "https://fresno.legistar.com/MeetingDetail.aspx?ID=925233&GUID=F1C9A953-1959-481E-B70D-FCECD8285489&Options=info|&Search=", # noqa
            "titleAgenda": "Meeting Agenda",
            "titleMeetingDetails": "Meeting Details",
        }
    ]


def test_classification():
    assert parsed_items[1]["classification"] == ADVISORY_COMMITTEE


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
