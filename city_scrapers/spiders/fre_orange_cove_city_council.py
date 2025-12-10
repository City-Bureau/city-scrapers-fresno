import re
from datetime import datetime

from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class FreOrangeCoveCityCouncilSpider(CityScrapersSpider):
    name = "fre_orange_cove_city_council"
    agency = "Orange Cove City Council"
    timezone = "America/Los_Angeles"
    start_urls = ["https://cityoforangecove.com/agendas/"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        # Get current year and previous year to scrape recent meetings
        current_year = datetime.now().year
        years_to_scrape = [str(current_year), str(current_year - 1)]

        for year in years_to_scrape:
            # Select meetings from this year's div
            for item in response.css(
                f"div[id='{year}'] div.vc_tta-panel-body div.wpb_wrapper p"
            ):
                meetingRaw = item.css("a::text").get()

                # Skip if no link text or if it contains "ITEM#"
                if not meetingRaw or "ITEM#" in meetingRaw:
                    continue

                # Check if the text contains a date pattern for the current year
                # Pattern matches: "Month Day, Year" or "MONTH DAY, YEAR"
                if re.search(rf"\d{{1,2}},?\s*{year}", meetingRaw, re.IGNORECASE):
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
        titleRaw = item.css("a::text").get()
        # Remove the date portion and extract the meeting type/title
        # Handle formats like "December 10, 2025 – Regular Council Meeting"
        # or "JANUARY 6, 2022 PUBLIC WORKSHOP"
        title_parts = re.split(r"\d{4}", titleRaw, 1)
        if len(title_parts) > 1:
            # Get everything after the year
            title = title_parts[1].strip()
            # Remove leading separators like "–", "-", or extra spaces
            title = re.sub(r"^[\s\–\-]+", "", title)
            return title if title else "City Council Meeting"
        # Fallback to original logic if date format is different
        parts = re.split(" ", titleRaw, 3)
        return parts[3] if len(parts) > 3 else "City Council Meeting"

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        dateRaw = item.css("a::text").get()

        # Extract date using regex to handle various formats
        # Matches "Month DD, YYYY" or "MONTH DD, YYYY"
        date_match = re.search(
            r"([A-Za-z]+)\s+(\d{1,2}),?\s*(\d{4})", dateRaw
        )

        if date_match:
            month = date_match.group(1)
            day = date_match.group(2)
            year = date_match.group(3)

            date = f"{month} {day} {year}"
            dt_obj = date + " " + "00:00:00"
            return parser().parse(dt_obj)

        # Fallback to None if date cannot be parsed
        return None

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return "Meeting time in unscrapable from this site, please check the meeting agenda link for meeting start time."  # noqa

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "699 6th Street, Orange Cove, California 93646",
            "name": "Senior Center",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": item.css("a::attr(href)").get(), "title": "Meeting Agenda"}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
