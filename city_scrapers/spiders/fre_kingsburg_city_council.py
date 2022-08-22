import ssl

from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser

ssl._create_default_https_context = ssl._create_unverified_context


class FreKingsburgCityCouncilSpider(CityScrapersSpider):
    name = "fre_kingsburg_city_council"
    agency = "Kingsburg City Council"
    timezone = "America/Chicago"
    start_urls = ["https://www.cityofkingsburg-ca.gov/agendacenter"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("div[id='cat9'] .catAgendaRow"):
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
        titleRaw = (item.css("td:nth-child(1) p a::text ").get()).strip()
        title = titleRaw.split("Agenda")
        return title[0]

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        month = item.css("td:nth-child(1) h4 strong abbr::text").get()
        dayYear = item.css("td:nth-child(1) h4 strong::text").get()

        dt_obj = month + " " + dayYear + " 14:00:00"
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
            "address": "1401 Draper Street, Kingsburg, CA 93631",
            "name": "Council Chamber",
        }

    def _parse_links(self, item):
        """Parse or generate links."""

        return [
            {
                "href": "https://www.cityofkingsburg-ca.gov"
                + item.css("td:nth-child(1) p a::attr(href)").get(),  # noqa
                "title": "Meeting Agenda",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
