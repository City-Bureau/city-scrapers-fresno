from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fresno_planning_commission import (
    FresnoPlanningCommissionSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fresno_planning_commission.html"),
    url=(
        "https://www.co.fresno.ca.us/departments/public-works-planning/"
        "divisions-of-public-works-and-planning/development-services-division/"
        "planning-and-land-use/planning-commission/plann/-toggle-allupcoming"
    ),
)
spider = FresnoPlanningCommissionSpider()

freezer = freeze_time("2022-08-07")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Planning Commission Meeting"


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 11, 8, 45)


def test_end():
    assert parsed_items[0]["end"] == datetime(2022, 8, 11, 12, 59)
