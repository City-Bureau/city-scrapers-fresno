import re
import ssl

from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser

ssl._create_default_https_context = ssl._create_unverified_context


class LemooreCityCouncilSpider(CityScrapersSpider):
    name = "fre_lemoore_city_council"
    agency = "Lemoore City Council"
    timezone = "America/Los_Angeles"
    start_urls = ["https://lemoore.com/councilagendas"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("div[id='elementor-tab-content-7431'] table tr")[1:]:
            date = item.css("td:nth-child(1)::text").get()
            if date.strip() and "CX" not in date:
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
        return "Lemoore City Council"

    def _parse_description(self, item):
        """Parse or generate meeting description."""

        title = (item.css("td:nth-child(1)::text").get()).strip()

        if "SP" in title:
            return "Lemoore City Council Special Meeting"
        else:
            return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""

        # css selector to get string that contains date and time
        date_raw = (item.css("td:nth-child(1)::text").get()).strip()

        # extract date from string
        # date = re.findall(r"\w+ \d{1,2}, \d{4}", date_raw)[0]
        date = re.findall(r"\w+ \d{1,2}, \d{4}", date_raw)[0]

        # meetings are at 5:30PM
        time = "17:30:00"

        # time changes are noted on the timeChanged string
        # assume evening time for city council meeting
        timeChanged = re.findall(r"\d{1,2}:\d{1,2}", date_raw)
        if timeChanged:
            time = timeChanged[0] + " pm"

        # combine date and time to get complete dt_obj
        dt_obj = date + " " + time

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
            "address": "429 C Street, Lemoore CA 93245",
            "name": "Lemoore Council Chambers",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "hrefAgenda": item.css("td:nth-child(2) a::attr(href)").get(),
                "titleAgenda": "Agenda",
                "hrefAgendaPacket": item.css("td:nth-child(3) a::attr(href)").get(),
                "titlePacket": "Agenda Packet",
                "hrefHandout": item.css("td:nth-child(4) a::attr(href)").get(),
                "titleHandout": "Handout",
                "hrefAudio": item.css(
                    "td:nth-child(6) a:nth-child(1)::attr(href)"
                ).get(),
                "titleAudio": "Meeting Audio",
                "hrefVideo": item.css(
                    "td:nth-child(6) a:nth-child(2)::attr(href)"
                ).get(),
                "titleVideo": "Meeting Video",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
