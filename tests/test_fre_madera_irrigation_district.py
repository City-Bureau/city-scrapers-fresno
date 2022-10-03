from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_madera_irrigation_district import (
    FreMaderaIrrigationDistrictSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fre_madera_irrigation_district.html"),
    url="https://www.madera-id.org/governance/agendas-and-minutes/2022-agendas-and-minutes/",  # noqa
)
spider = FreMaderaIrrigationDistrictSpider()

freezer = freeze_time("2022-09-30")
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
    assert parsed_items[0]["title"] == "MID-GSA Agenda"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 9, 20, 13, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_madera_irrigation_district/202209201300/x/mid_gsa_agenda"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Madera Irrigation District",
        "address": "12152 Road 28 ¼, Madera, California 93637",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.madera-id.org/governance/agendas-and-minutes/2022-agendas-and-minutes/"  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.madera-id.org/wp-content/uploads/2022/09/22-09-20-MID-GSA-Agenda.pdf",  # noqa
            "title": "Meeting Link",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
