from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class SanJoaquinValleyAirPollutionSpider(CityScrapersSpider):
    name = "fre_san_joaquin_valley_air_pollution"
    agency = "San Joaquin Valley Air Pollution Control District"
    timezone = "America/Los_Angeles"
    current_year = datetime.now().year
    start_urls = [
        f"https://www.valleyair.org/public-meetings-and-participation/governing-board/?year={current_year}",
        f"https://www.valleyair.org/public-meetings-and-participation/governing-board/?year={current_year - 1}",
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        # Find the table with Meeting Date header
        for item in response.css("table tbody tr"):
            # Check if this row has a date (first cell should contain text)
            date_text = item.css("td:nth-child(1)::text").get()
            if date_text and date_text.strip():
                meeting = Meeting(
                    title=self._parse_title(item),
                    description=self._parse_description(item),
                    classification=self._parse_classification(item),
                    start=self._parse_start(item, response),
                    end=self._parse_end(item),
                    all_day=self._parse_all_day(item),
                    time_notes=self._parse_time_notes(item),
                    location=self._parse_location(item),
                    links=self._parse_links(item, response),
                    source=self._parse_source(response),
                )

                meeting["status"] = self._get_status(meeting)
                meeting["id"] = self._get_id(meeting)

                yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return (
            "San Joaquin Valley Unified Air Pollution Control District Governing Board"
        )

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item, response):
        """Parse start datetime as a naive datetime object."""
        import re

        date_text = item.css("td:nth-child(1)::text").get()
        if not date_text:
            return None

        # Extract year from URL query parameter
        year_match = re.search(r"year=(\d{4})", response.url)
        year = year_match.group(1) if year_match else str(datetime.now().year)

        # Clean the date text and add year
        date_text = date_text.strip()
        # Handle "and X Study Session" text
        date_text = re.sub(r"\s+and.*$", "", date_text)
        # Handle "Special Public Hearing" and similar extra text
        date_text = re.sub(r"\s+Special.*$", "", date_text)
        date_text = re.sub(r"\s+Public.*$", "", date_text)

        time = "9:00 AM"
        dt_string = f"{date_text} {year} {time}"
        return parser().parse(dt_string)

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
            "address": "1990 E. Gettysburg Avenue, Fresno, CA",
            "name": "Central Region Office, Governing Board Room",
        }

    def _parse_links(self, item, response):
        """Parse or generate links."""
        links = []

        # Agenda - column 2
        agenda_href = item.css("td:nth-child(2) a::attr(href)").get()
        if agenda_href:
            if agenda_href.startswith("http"):
                agenda_url = agenda_href
            else:
                agenda_url = response.urljoin(agenda_href)
            links.append({"href": agenda_url, "title": "Agenda"})

        # Minutes - column 3
        minutes_href = item.css("td:nth-child(3) a::attr(href)").get()
        if minutes_href:
            if minutes_href.startswith("http"):
                minutes_url = minutes_href
            else:
                minutes_url = response.urljoin(minutes_href)
            links.append({"href": minutes_url, "title": "Minutes"})

        # Presentations - column 4
        presentations_href = item.css("td:nth-child(4) a::attr(href)").get()
        if presentations_href:
            if presentations_href.startswith("http"):
                presentations_url = presentations_href
            else:
                presentations_url = response.urljoin(presentations_href)
            links.append({"href": presentations_url, "title": "Presentations"})

        # Video/Recording - column 5
        recording_href = item.css("td:nth-child(5) a::attr(href)").get()
        if recording_href:
            links.append({"href": recording_href, "title": "Recording"})

        return links

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
