from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED, PASSED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_mendota_city_council import FreMendotaCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_mendota_city_council.html"),
    url="https://www.cityofmendota.com/agendas-and-minutes/",
)
spider = FreMendotaCityCouncilSpider()

freezer = freeze_time(datetime(2024, 4, 24, 13, 52))
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]
parsed_item = parsed_items[0]
freezer.stop()


def test_title():
    assert parsed_item["title"] == "April 23, 2024"


def test_description():
    assert parsed_item["description"] == ""


def test_start():
    assert parsed_item["start"] == datetime(2024, 4, 23, 18, 0)


def test_end():
    assert parsed_item["end"] is None


def test_time_notes():
    assert parsed_item["time_notes"] == ""


def test_id():
    assert parsed_item["id"] == "fre_mendota_city_council/202404231800/x/april_23_2024"


def test_status():
    assert parsed_item["status"] == PASSED


def test_location():
    assert parsed_item["location"] == {"address": "", "name": ""}


def test_source():
    assert parsed_item["source"] == "https://www.cityofmendota.com/agendas-and-minutes/"


def test_links():
    assert parsed_item["links"] == [
        {
            "href": "https://www.cityofmendota.com/wp-content/uploads/2024/04/4-23-24-City-Council-Meeting-Amended-Agenda-Packet.pdf",  # noqa
            "title": "Amended Agenda (English)",
        }
    ]


def test_classification():
    assert parsed_item["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
