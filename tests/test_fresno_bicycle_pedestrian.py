from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import ADVISORY_COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fresno_bicycle_pedestrian import FresnoBicyclePedestrianSpider

test_response = file_response(
    join(dirname(__file__), "files", "fresno_bicycle_pedestrian.html"),
    url="https://fresno.legistar.com/Calendar.aspx",
)
spider = FresnoBicyclePedestrianSpider()

freezer = freeze_time("2022-08-08")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

'''
freezer = freeze_time("2022-08-08")
freezer.start()

with open(join(dirname(__file__), "files", "fresno_bicycle_pedestrian.json"), "r", encoding="utf-8") as f:
    test_response = json.load(f)

spider = FresnoBicyclePedestrianSpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

freezer.stop()
'''

"""
def test_tests():
    print("Please write some tests for this spider or at least disable this one.")
    assert False

Uncomment below
"""

#def test_title():
    #assert parsed_items[0]["title"] == "Bicycle and Pedestrian Advisory Committee"

# def test_description():
#     assert parsed_items[0]["description"] == "EXPECTED DESCRIPTION"


# def test_start():
#     assert parsed_items[0]["start"] == datetime(2019, 1, 1, 0, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


# def test_time_notes():
#     assert parsed_items[0]["time_notes"] == "EXPECTED TIME NOTES"


# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"


# def test_status():
#     assert parsed_items[0]["status"] == "EXPECTED STATUS"


# def test_location():
#     assert parsed_items[0]["location"] == {
#         "name": "EXPECTED NAME",
#         "address": "EXPECTED ADDRESS"
#     }


# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"


# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]


def test_classification():
    assert parsed_items[1]["classification"] == ADVISORY_COMMITTEE


#@pytest.mark.parametrize("item", parsed_items)
# def test_all_day(item):
#     assert item["all_day"] is False
