from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_fresno_housing import FresnoHousingSpider

test_response = file_response(
    join(dirname(__file__), "files", "fresno_housing.html"),
    url="https://fresnohousing.org/about-us/board-documents-2022/",
)
spider = FresnoHousingSpider()

freezer = freeze_time("2022-08-07")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

"""
Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"] == "Regular Board Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 1, 25, 13, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "fre_housing/202201251300/x/regular_board_meeting"


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "1260 Fulton Street (2nd Floor), Fresno, CA. 93721",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://fresnohousing.org/about-us/board-documents-2022/"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://fresnohousing.org/wp-content/uploads/2022/01/01.25.22-Board-Meeting-Packet-v2.pdf",  # noqa
            "title": "Meeting Packet",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == "Board"
