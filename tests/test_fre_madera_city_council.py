from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_madera_city_council import FreMaderaCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_madera_city_council.html"),
    url="http://www.madera.gov/home/departments/city-clerk/city-council-agendas-meetings/#tr-2022-meetings-4850011", # noqa
)
spider = FreMaderaCityCouncilSpider()

freezer = freeze_time("2022-08-21")
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
    assert parsed_items[0]["title"] == "Special Meeting of the Madera City Council"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 24, 18, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_madera_city_council/202208241800/x/special_meeting_of_the_madera_city_council" # noqa
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chambers, City Hall",
        "address": "205 W. 4th Street, Madera, California 93637",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.madera.gov/home/departments/city-clerk/city-council-agendas-meetings/" # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "hrefAgenda": "https://www.madera.gov/wp-content/uploads/2022/08/08.24.22s-Final-Agenda.pdf", # noqa
            "hrefReport": "https://www.madera.gov/wp-content/uploads/2022/08/08.24.22s-Final-Links.pdf", # noqa
            "hrefVideo": None,
            "titleAgenda": "Agenda",
            "titleReport": "Report",
            "titleVideo": "Video",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
