from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_reedley_city_council import FreReedleyCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_reedley_city_council.html"),
    url="https://reedley.ca.gov/city-council/city-council-agendas/",
)
spider = FreReedleyCityCouncilSpider()

freezer = freeze_time("2022-08-29")
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
    assert parsed_items[0]["title"] == "Regular Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


# def test_start():
#     assert parsed_items[0]["start"] == datetime(2022, 9, 27, 19, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == ""


# def test_id():
#     assert parsed_items[0]["id"] == "fre_reedley_city_council/202209271900/x/regular_meeting"  # noqa


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chambers",
        "address": "845 'G' Street, Reedley, California ",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://reedley.ca.gov/city-council/city-council-agendas/"
    )


"""
def test_links():
    assert parsed_items[0]["links"] == [{
      "href": "https://reedley.ca.gov/download/sep-27-city-council-agenda-3/?wpdmdl=16361&refresh=6335940f040171664455695",  # noqa
      "title": "Agenda"
    }]
"""


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
