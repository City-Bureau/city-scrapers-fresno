from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, COMMITTEE, NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.friant_water_authority import FriantWaterAuthoritySpider

test_response = file_response(
    join(dirname(__file__), "files", "friant_water_authority.html"),
    url="https://friantwater.org/meetings-events",
)
spider = FriantWaterAuthoritySpider()

freezer = freeze_time("2022-09-25")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Kaweah Delta WCD BM"
    assert parsed_items[1]["title"] == "Pixley ID BM"
    assert parsed_items[2]["title"] == "Friant Division Manager's Group Meeting"
    assert parsed_items[3]["title"] == "Lower Tule River ID BM"
    assert parsed_items[4]["title"] == "Tulare ID BM"
    assert parsed_items[5]["title"] == "Porterville ID BM"
    assert parsed_items[6]["title"] == "Arvin-Edison WSD BM"


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 10, 4, 9, 0)
    assert parsed_items[1]["start"] == datetime(2022, 10, 6, 9, 0)
    assert parsed_items[2]["start"] == datetime(2022, 10, 7, 8, 30)
    assert parsed_items[3]["start"] == datetime(2022, 10, 11, 9, 0)
    assert parsed_items[4]["start"] == datetime(2022, 10, 11, 9, 0)
    assert parsed_items[5]["start"] == datetime(2022, 10, 11, 9, 0)
    assert parsed_items[6]["start"] == datetime(2022, 10, 11, 12, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2022, 10, 4, 10, 0)
    assert parsed_items[1]["end"] == datetime(2022, 10, 6, 10, 0)
    assert parsed_items[2]["end"] == datetime(2022, 10, 7, 10, 0)
    assert parsed_items[3]["end"] == datetime(2022, 10, 11, 10, 0)
    assert parsed_items[4]["end"] == datetime(2022, 10, 11, 10, 0)
    assert parsed_items[5]["end"] == datetime(2022, 10, 11, 10, 0)
    assert parsed_items[6]["end"] == datetime(2022, 10, 11, 13, 0)


def test_id():
    assert parsed_items[0]["id"] == (
        "friant_water_authority/" "202210040900/x/kaweah_delta_wcd_bm"
    )
    assert parsed_items[1]["id"] == (
        "friant_water_authority/" "202210060900/x/pixley_id_bm"
    )
    assert parsed_items[2]["id"] == (
        "friant_water_authority/"
        "202210070830/x/"
        "friant_division_manager_s_group_meeting"
    )
    assert parsed_items[3]["id"] == (
        "friant_water_authority/202210110900/x/lower_tule_river_id_bm"
    )
    assert parsed_items[4]["id"] == (
        "friant_water_authority/202210110900/x/tulare_id_bm"
    )
    assert parsed_items[5]["id"] == (
        "friant_water_authority/202210110900/x/porterville_id_bm"
    )
    assert parsed_items[6]["id"] == (
        "friant_water_authority/202210111200/x/arvin_edison_wsd_bm"
    )


def test_status():
    for i in range(0, 107):
        if i < 77:
            assert parsed_items[i]["status"] == "tentative"
        else:
            assert parsed_items[i]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Kaweah Delta WCD",
        "address": ("2975 Farmersville Road Farmersville, CA, 93223 United States"),
    }
    assert parsed_items[1]["location"] == {
        "name": "Pixley ID",
        "address": "357 East Olive Avenue Tipton, CA, 93272 United States",
    }
    assert parsed_items[2]["location"] == {
        "name": "Friant Water Authority",
        "address": "854 N Harvard Ave Lindsay, CA 93247 United States",
    }
    assert parsed_items[3]["location"] == {
        "name": "Lower River Tule ID",
        "address": "357 East Olive Avenue Tipton, CA, 93272 United States",
    }
    assert parsed_items[4]["location"] == {
        "name": "Tulare ID",
        "address": "6826 Avenue 240 Tulare CA 93274",
    }
    assert parsed_items[5]["location"] == {
        "name": "Porterville ID",
        "address": "22086 Avenue 160 Porterville, CA, 93257 United States",
    }
    assert parsed_items[6]["location"] == {
        "name": "Arvin-Edison WSD",
        "address": (
            "20401 Bear Mountain Boulevard Bakersfield, CA, 93311 United States"
        ),
    }


@pytest.mark.parametrize("item", parsed_items)
def test_source(item):
    assert item["source"] == ("https://friantwater.org/meetings-events")


def test_links():
    assert parsed_items[104]["links"] == [
        {
            "href": (
                "/s/NEW-Meeting-Book-FWA-Finance-HR-"
                "Committee-Meeting-August-22-2022-1.pdf"
            ),
            "title": (
                "NEW-Meeting-Book-FWA-Finance-HR-Committee-Meeting-August-22-2022-1"
            ),
        },
        {
            "href": (
                "http://maps.google.com?q=854 North Harvard Avenue "
                "Lindsay, CA, 93247 United States"
            ),
            "title": "Friant Water Authority Map Link",
        },
    ]

    assert parsed_items[105]["links"] == [
        {
            "href": (
                "http://maps.google.com?q=12152 Road 28 1/4 Madera, CA, "
                "93637 United States"
            ),
            "title": "Madera ID Map Link",
        }
    ]

    assert parsed_items[106]["links"] == [
        {
            "href": (
                "/s/FINAL-August-Meeting-Book-FWA-"
                "Executive-Committee-Meeting-August-15-2022-3.pdf"
            ),
            "title": (
                "FINAL-August-Meeting-Book-FWA-"
                "Executive-Committee-Meeting-August-15-2022-3"
            ),
        },
        {
            "href": (
                "http://maps.google.com?q=854 N Harvard "
                "Ave Lindsay, CA 93247 United States"
            ),
            "title": "Friant Water Authority Map Link",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD
    assert parsed_items[1]["classification"] == BOARD
    assert parsed_items[2]["classification"] == NOT_CLASSIFIED
    assert parsed_items[3]["classification"] == BOARD
    assert parsed_items[4]["classification"] == BOARD
    assert parsed_items[5]["classification"] == BOARD
    assert parsed_items[6]["classification"] == BOARD
    assert parsed_items[22]["classification"] == COMMITTEE


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
