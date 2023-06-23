import ssl

from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser

ssl._create_default_https_context = ssl._create_unverified_context


class FreFarmersvilleCityCouncilSpider(CityScrapersSpider):
    name = "fre_farmersville_city_council"
    agency = "Farmersville City Council"
    timezone = "America/Los_Angeles"
    start_urls = ["https://www.cityoffarmersville-ca.gov/agendacenter"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("table[id='table2'] tr td:nth-child(1)")[1:]:
            title = (item.css("p a::text").get()).strip()
            if "Cancellation" not in title:
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

        title = (item.css("p a::text").get()).strip()

        print(title)

        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""

        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""

        date = item.css("h4 strong::attr(aria-label)").get()

        dateExtract = date.split(" ", 2)[2]

        dt_obj = dateExtract + " " + "18:00:00"

        return parser().parse(dt_obj)

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return "Time is unscrapable from this website, meeting time is assumed to be the standard 6:00PM time. Please check the meeting agenda link to confirm time."  # noqa

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "909 West Visalia Road Farmersville, California",
            "name": "Civic Center Chamber Council",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "href": "https://www.cityoffarmersville-ca.gov"
                + item.css("p a::attr(href)").get(),
                "title": "Agenda",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
