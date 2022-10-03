from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import (CITY_COUNCIL,
                                          COMMISSION,
                                          NOT_CLASSIFIED)
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_fowler_city_council import FreFowlerCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "fre_fowler_city_council.html"),
    url="https://fowlercity.org/agendas-minutes/",
)
spider = FreFowlerCityCouncilSpider()

freezer = freeze_time("2022-10-02")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "City Council 2022: October 4, 2022\xa0 Agenda"
    assert parsed_items[1]["title"] == "City Council 2022: September 20, 2022\xa0 Agenda"
    assert parsed_items[2]["title"] == "City Council 2022: September 6, 2022 City Council Meeting Cancelled"
    assert parsed_items[3]["title"] == "City Council 2022: August 16, 2022\xa0 Agenda"
    assert parsed_items[4]["title"] == "City Council 2022: August 2, 2022\xa0 Agenda"
    assert parsed_items[5]["title"] == "City Council 2022: July 25, 2022\xa0 Special Meeting Agenda"
    assert parsed_items[6]["title"] == "City Council 2022: July 19, 2022\xa0 Agenda"


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 10, 4, 19, 0)
    assert parsed_items[1]["start"] == datetime(2022, 9, 20, 19, 0)
    assert parsed_items[2]["start"] == datetime(2022, 9, 6, 19, 0)
    assert parsed_items[3]["start"] == datetime(2022, 8, 16, 19, 0)
    assert parsed_items[4]["start"] == datetime(2022, 8, 2, 19, 0)
    assert parsed_items[5]["start"] == datetime(2022, 7, 25, 19, 0)
    assert parsed_items[6]["start"] == datetime(2022, 7, 19, 19, 0)


@pytest.mark.parametrize("item", parsed_items)
def test_time_notes(item):
    assert item["time_notes"] == ("Meetings regularly take place at "
                                  "7:00 PM PST, but are subject "
                                  "to change. Refer to agenda if available.")


def test_id():
    assert parsed_items[0]["id"] == "fre_fowler_city_council/202210041900/x/city_council_2022_october_4_2022_agenda"
    assert parsed_items[1]["id"] == "fre_fowler_city_council/202209201900/x/city_council_2022_september_20_2022_agenda"
    assert parsed_items[2]["id"] == "fre_fowler_city_council/202209061900/x/city_council_2022_september_6_2022_city_council_meeting"
    assert parsed_items[3]["id"] == "fre_fowler_city_council/202208161900/x/city_council_2022_august_16_2022_agenda"
    assert parsed_items[4]["id"] == "fre_fowler_city_council/202208021900/x/city_council_2022_august_2_2022_agenda"
    assert parsed_items[5]["id"] == "fre_fowler_city_council/202207251900/x/city_council_2022_july_25_2022_special_meeting_agenda"
    assert parsed_items[6]["id"] == "fre_fowler_city_council/202207191900/x/city_council_2022_july_19_2022_agenda"


def test_status():
    assert parsed_items[0]["status"] == "tentative"
    assert parsed_items[1]["status"] == "passed"
    assert parsed_items[2]["status"] == "cancelled"
    assert parsed_items[3]["status"] == "passed"
    assert parsed_items[4]["status"] == "passed"
    assert parsed_items[5]["status"] == "passed"
    assert parsed_items[6]["status"] == "passed"


@pytest.mark.parametrize("item", parsed_items)
def test_location(item):
    assert item["location"] == {
        "address": "128 SOUTH 5TH STREET FOWLER, CA 93625",
        "name": "CITY COUNCIL CHAMBER"
    }


def test_source():
    assert parsed_items[0]["source"] == "https://fowlercity.org/agendas-minutes/"


def test_links():
    assert parsed_items[0]["links"] == [{
        "href": "https://fowlercity.org/wp-content/uploads/2022/09/FCC-Agenda-10042022.pdf",
        "title": "FCC-Agenda-10042022"
    }]
    assert parsed_items[1]["links"] == [{
            "href": "https://fowlercity.org/wp-content/uploads/2022/09/FCC-Agenda-09202022.pdf",
            "title": "FCC-Agenda-09202022"
        },
        {
            "href": "https://fowlercity.org/wp-content/uploads/2022/09/FCC-SP-Agenda-09202022.pdf",
            "title": "FCC-SP-Agenda-09202022"
    }]
    assert parsed_items[2]["links"] == [{
        "href": "https://fowlercity.org/wp-content/uploads/2022/09/FCC-Cancelled-09062022.pdf",
        "title": "FCC-Cancelled-09062022"
    }]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL
    assert parsed_items[1]["classification"] == CITY_COUNCIL
    assert parsed_items[2]["classification"] == CITY_COUNCIL
    assert parsed_items[3]["classification"] == CITY_COUNCIL
    assert parsed_items[4]["classification"] == CITY_COUNCIL
    assert parsed_items[5]["classification"] == CITY_COUNCIL
    assert parsed_items[6]["classification"] == CITY_COUNCIL
    assert parsed_items[len(parsed_items)-1]["classification"] == COMMISSION


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
