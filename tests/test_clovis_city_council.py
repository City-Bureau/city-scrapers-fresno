from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_clovis_city_council import ClovisCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "clovis_city_council.html"),
    url="https://meetings.municode.com/PublishPage?cid=CLOVIS&ppid=5157d66d-a361-43e8-87a4-3d5eca4821de&p=1",  # noqa
)
spider = ClovisCityCouncilSpider()

freezer = freeze_time("2022-08-10")
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
    assert parsed_items[0]["title"] == "City Council Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 1, 18, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_clovis_city_council/202208011800/x/city_council_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Clovis City Council",
        "address": "1033 Fifth Street, Clovis, CA 93612",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://meetings.municode.com/PublishPage?cid=CLOVIS&ppid=5157d66d-a361-43e8-87a4-3d5eca4821de&p=1"  # noqa
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://meetings.municode.com/d/f?u=https://mccmeetings.blob.core.usgovcloudapi.net/clovis-pubu/MEET-Agenda-7b1add8e8e3441b7aa5d36b337aacb2c.pdf&n=Agenda-City%20Council%20Meeting-August 1, 2022 6.00 PM.pdf"  # noqa
            + " https://meetings.municode.com/d/f?u=https://mccmeetings.blob.core.usgovcloudapi.net/clovis-pubu/MEET-Packet-7b1add8e8e3441b7aa5d36b337aacb2c.pdf&n=AgendaPacket-City%20Council%20Meeting-August 1, 2022 6.00 PM.pdf",  # noqa
            "title": "Meeting Agenda and Meeting Packet",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == "City Council"


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
