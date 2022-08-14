from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser
import re


class AvenalCityCouncilSpider(CityScrapersSpider):
    name = "avenal_city_council"
    agency = "Avenal City Council"
    timezone = "America/Chicago"
    start_urls = ["https://www.cityofavenal.com/agendacenter"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("table[id='table1'] tr td:nth-child(1)"):
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

        titleRaw = item.css("p a::text").get()

        title = titleRaw.strip()

        titleExtract = title.split(":")[0]

        return titleExtract

    def _parse_description(self, item):
        """Parse or generate meeting description."""

        descriptionRaw = item.css("p a::text").get()

        description = descriptionRaw.strip()

        descriptionExtract = description.split(":")[1]

        return descriptionExtract

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""

        date = item.css("h4 strong::attr(aria-label)").get()

        dateExtract = date.split(" ", 2)[2]

        dt_obj = dateExtract + " " + "12:41:15.281060"
        
        return parser().parse(dt_obj)

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
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "https://www.cityofavenal.com/" + item.css("p a::attr(href)").get(), 
                "title": "Agenda"
        }]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
