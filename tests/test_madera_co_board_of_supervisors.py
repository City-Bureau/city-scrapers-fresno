from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_madera_co_board_of_supervisors import (
    MaderaCoBoardOfSupervisorsSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "madera_co_board_of_supervisors.html"),
    url=(
        "https://www.maderacounty.com/services/advanced-components/"
        "list-detail-pages/calendar-meeting-list/-npage-2/-seldept-6"
    ),
)
spider = MaderaCoBoardOfSupervisorsSpider()

freezer = freeze_time("2022-08-07")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Board of Supervisors Regular Meeting"


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 9, 10, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2022, 8, 9, 13, 0)
