import re

from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class FreSelmaCityCouncilSpider(CityScrapersSpider):
    name = "fre_selma_city_council"
    agency = "Selma City Council"
    timezone = "America/Chicago"
    start_urls = [
        "https://www.cityofselma.com/government/city_council/council_meetings___agendas.php"  # noqa
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("table"):

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
        title = ""
        titleRaw = item.css("tr td:nth-child(1)::text").get()
        if "Regular" in titleRaw:
            title = "Regular Meeting"
        else:
            title = "Special Meeting"

        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        dateRaw = (item.css("tr td:nth-child(1)::text").get()).strip()
        date = re.findall(r"\d{1,2}/\d{1,2}/\d{1,2}", dateRaw)[0]
        dt_obj = date + " " + "14:00:00"
        return parser().parse(dt_obj)

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        title = item.css("tr td:nth-child(1)::text").get()
        if "Special Meeting" in title:
            return "Double check Agenda for start time of Special City Council meetings"

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""

        return {
            "address": "1710 Tucker Street, Selma, California",
            "name": "Council Chambers",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        agenda = ""
        packet = ""

        if item.css("tr td:nth-child(2) a:nth-child(1)::attr(href)").get():
            agenda = item.css("tr td:nth-child(2) a:nth-child(1)::attr(href)").get()
        else:
            agenda = "No Agenda"

        if item.css("tr td:nth-child(2) a:nth-child(2)::attr(href)").get():
            packet = item.css("tr td:nth-child(2) a:nth-child(2)::attr(href)").get()
        else:
            packet = "No Packet"

        return [
            {
                "hrefAgenda": "https://cms9files.revize.com/selma/" + agenda,
                "titleAgenda": "Agenda",
                "hrefPacket": "https://cms9files.revize.com/selma/" + packet,
                "titlePacket": "Packet",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
