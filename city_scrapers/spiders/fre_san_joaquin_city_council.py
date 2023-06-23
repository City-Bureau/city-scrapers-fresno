from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class FreSanJoaquinCityCouncilSpider(CityScrapersSpider):
    name = "fre_san_joaquin_city_council"
    agency = "San Joaquin City Council"
    timezone = "America/Los_Angeles"
    start_urls = ["https://www.cityofsanjoaquin.org/government.html"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(
            "body div.content div.row div.row div.row div.column ul.a li"
        ):
            meetingDate = item.css("p::text").get()

            if "2022" in meetingDate:
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
            else:
                return

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return "San Joaquin City Council"

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        startDate = item.css("p::text").get()
        dt_obj = startDate + " " + "18:00:00"
        return parser().parse(dt_obj)

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return "Time is unscrapable from this website, meeting time is assumed to be 6:00PM as noted on the website. Please check the agenda link to confirm meeting time."  # noqa

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "21991 Colorado Avenue, San Joaquin, CA",
            "name": "Senior Center",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "href": "https://www.cityofsanjoaquin.org/"
                + item.css("a::attr(href)").get(),
                "title": "Agenda",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
