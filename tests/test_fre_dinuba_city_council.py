from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_dinuba_city_council import FreDinubaCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_dinuba_city_council.html"),
    url="https://dinuba.novusagenda.com/agendapublic/meetingsgeneral.aspx?MeetingType=1&Date=6ms",  # noqa
)
spider = FreDinubaCityCouncilSpider()

freezer = freeze_time("2022-10-01")
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
    assert parsed_items[0]["title"] == "City Council"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 9, 27, 18, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"] == "fre_dinuba_city_council/202209271830/x/city_council"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chambers",
        "address": "405 E El Monte Way, Dinuba CA 93618",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://dinuba.novusagenda.com/agendapublic/meetingsgeneral.aspx?MeetingType=1&Date=6ms"  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "hrefAgenda": "https://dinuba.novusagenda.com/agendapublic/DisplayAgendaPDF.ashx?MeetingID=365",  # noqa
            "titleAgenda": "Agenda PDF",
        },
        {
            "hrefPage": "https://dinuba.novusagenda.com/agendapublic/MeetingView.aspx?MeetingID=365&MinutesMeetingID=302&doctype=Agenda",  # noqa
            "titlePage": "Agenda Page",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
