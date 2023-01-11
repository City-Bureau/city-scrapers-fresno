from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_clovis_planning import ClovisPlanningSpider

test_response = file_response(
    join(dirname(__file__), "files", "clovis_planning.html"),
    url=(
        "https://meetings.municode.com/PublishPage?cid=CLOVIS"
        "&ppid=ad6551de-2ee0-4b3f-b2ab-803f5aca27c8&p=1"
    ),
)
spider = ClovisPlanningSpider()

freezer = freeze_time("2022-08-07")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "July 28, 2022 Planning Commission Meeting"


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 7, 28, 18, 0)


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "",
        "address": "Council Chambers 1033 Fifth Street Clovis, CA 93612",
    }


def test_links():
    assert parsed_items[0]["links"][0]["title"] == "Agenda"
    assert parsed_items[0]["links"][1]["title"] == "Packet"
