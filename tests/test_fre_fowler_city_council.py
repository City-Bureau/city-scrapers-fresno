from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL, PASSED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_fowler_city_council import FreFowlerCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_fowler_city_council.html"),
    url="https://fowlercity.org/agendas-minutes/",
)
spider = FreFowlerCityCouncilSpider()

freezer = freeze_time(datetime(2024, 4, 24, 15, 39))
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]
parsed_item = parsed_items[0]
freezer.stop()


def test_title():
    assert parsed_item["title"] == "City Council 2024: April 16, 2024  Agenda"


def test_description():
    assert parsed_item["description"] == ""


def test_start():
    assert parsed_item["start"] == datetime(2024, 4, 16, 19, 0)


def test_end():
    assert parsed_item["end"] is None


def test_time_notes():
    assert (
        parsed_item["time_notes"]
        == "Meetings regularly take place at 7:00 PM PST, but are subject to change. Refer to agenda if available."  # noqa
    )


def test_id():
    assert (
        parsed_item["id"]
        == "fre_fowler_city_council/202404161900/x/city_council_2024_april_16_2024_agenda"  # noqa
    )


def test_status():
    assert parsed_item["status"] == PASSED


def test_location():
    assert parsed_item["location"] == {
        "address": "128 SOUTH 5TH STREET FOWLER, CA 93625",
        "name": "CITY COUNCIL CHAMBER",
    }


def test_source():
    assert parsed_item["source"] == "https://fowlercity.org/agendas-minutes/"


def test_links():
    assert parsed_item["links"] == [
        {
            "href": "https://fowlercity.org/wp-content/uploads/2024/04/FCC-Agenda-04162024.pdf",  # noqa
            "title": "FCC-Agenda-04162024",
        }
    ]


def test_classification():
    assert parsed_item["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
