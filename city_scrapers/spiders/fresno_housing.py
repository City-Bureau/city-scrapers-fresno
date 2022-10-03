import re
from datetime import date, datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class FresnoHousingSpider(CityScrapersSpider):
    name = "fre_housing"
    agency = "Fresno Housing Authority"
    timezone = "America/Los_Angeles"
    current_year = date.today().year
    start_urls = [
        f"https://fresnohousing.org/about-us/board-documents/board-documents-{current_year}/"  # noqa
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(".listitems li"):
            title = item.css(".left::text").get()
            if title:
                meeting = Meeting(
                    title=self._parse_title(item),
                    description=self._parse_description(item),
                    classification=self._parse_classification(item),
                    start=self._parse_start(item),
                    end=self._parse_end(item),
                    all_day=self._parse_all_day(item),
                    time_notes=self._parse_time_notes(item),
                    location=self._parse_location(item),
                    links=self._parse_links(item),
                    source=self._parse_source(response),
                )

                meeting["status"] = self._get_status(meeting)
                meeting["id"] = self._get_id(meeting)

                yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        title = item.css(".left::text").get()
        if "special" in title.lower():
            return "Special Board Meeting"
        return "Regular Board Meeting"

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        # all meetings start at 5:00PM
        meeting_time = "13:00:00"
        # obtain meeting title that contains meeting month and day
        title = item.css(".left::text").get()
        test_str = title
        result = re.findall(r"\w+ \d{1,2}, \d{4}", test_str)
        result2 = re.findall(r"\w+ \d{4}", test_str)
        if result:
            start = result[0] + " " + meeting_time
            return datetime.strptime(start, "%B %d, %Y %H:%M:%S")
        if result2:
            start = result2[0] + " " + meeting_time
            return datetime.strptime(start, "%B %Y %H:%M:%S")

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "1260 Fulton Street (2nd Floor), Fresno, CA. 93721",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        href = item.css(".readmore::attr(href)").get()
        return [{"href": href, "title": "Meeting Packet"}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
