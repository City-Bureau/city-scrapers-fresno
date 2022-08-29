from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.lemoore_city_council import LemooreCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "lemoore_city_council.html"),
    url="https://lemoore.com/councilagendas",
)
spider = LemooreCityCouncilSpider()

freezer = freeze_time("2022-08-14")
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
    assert parsed_items[0]["title"] == "Lemoore City Council"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 1, 4, 17, 30)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "lemoore_city_council/202201041730/x/lemoore_city_council"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Lemoore Council Chambers",
        "address": "429 C Street, Lemoore CA 93245",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://lemoore.com/councilagendas"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "hrefAgenda": "https://lemoore.com/wp-content/uploads/2021/12/Agenda-01-04-2022.pdf",  # noqa
            "titleAgenda": "Agenda",
            "hrefAgendaPacket": "https://lemoore.com/wp-content/uploads/2021/12/Electronic-Agenda-Packet-01-04-2022.pdf",  # noqa
            "titlePacket": "Agenda Packet",
            "hrefHandout": "https://lemoore.com/wp-content/uploads/2022/01/Handouts-received-after-agenda-posted-01-04-22.pdf",  # noqa
            "titleHandout": "Handout",
            "hrefAudio": "https://archive.org/details/city-of-lemoore-council-meeting-1-4-2022",  # noqa
            "titleAudio": "Meeting Audio",
            "hrefVideo": "https://www.youtube.com/watch?v=OQMsnEtMi_k",
            "titleVideo": "Meeting Video",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
