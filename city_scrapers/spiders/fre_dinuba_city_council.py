from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class FreDinubaCityCouncilSpider(CityScrapersSpider):
    name = "fre_dinuba_city_council"
    agency = "Dinuba City Council"
    timezone = "America/Los_Angeles"
    start_urls = [
        "https://dinuba.novusagenda.com/agendapublic/meetingsgeneral.aspx?MeetingType=1&Date=6ms"  # noqa
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(
            "div[id='SearchAgendasMeetings_radGridMeetings'] table.rgMasterTable:nth-child(1) tr"  # noqa
        )[1:]:
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
        return "City Council"

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        startDate = item.css("td:nth-child(1)::text").get()
        dt_obj = startDate + " 18:30:00"
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
            "address": item.css("td:nth-child(3)::text").get(),
            "name": "Council Chambers",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        hrefAgenda = (
            "https://dinuba.novusagenda.com/agendapublic/"
            + item.css("td:nth-child(5) a::attr(href)").get()
        )

        onclick = item.css("td:nth-child(4) a::attr(onclick)").get()
        substring = onclick.split("'", 1)[1]
        substring2 = substring.split("'", 1)[0]
        hrefPage = "https://dinuba.novusagenda.com/agendapublic/" + substring2

        return [
            {"hrefAgenda": hrefAgenda, "titleAgenda": "Agenda PDF"},
            {"hrefPage": hrefPage, "titlePage": "Agenda Page"},
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
