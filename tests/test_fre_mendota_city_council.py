from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_mendota_city_council import FreMendotaCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_mendota_city_council.html"),
    url="https://www.ci.mendota.ca.us/agendas-and-minutes/",
)
spider = FreMendotaCityCouncilSpider()

freezer = freeze_time("2022-09-29")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "September 27, 2022"


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 9, 27, 18, 0)


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.ci.mendota.ca.us/wp-content/uploads/2022/09/9-27-22-City-Council-Meeting-Agenda-Packet.pdf",  # noqa
            "title": "Agenda",
        }
    ]
