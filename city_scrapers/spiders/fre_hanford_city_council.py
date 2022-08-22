from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class FreHanfordCityCouncilSpider(CityScrapersSpider):
    name = "fre_hanford_city_council"
    agency = "Fresno Hanford City Council"
    timezone = "America/Chicago"
    start_urls = ["http://hanfordca.iqm2.com/Citizens/Calendar.aspx"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(
            "div[id='ContentPlaceholder1_pnlMeetings'] .MeetingRow"
        ):
            title = item.css(".RowBottom .RowDetails::text").get()
            titleSubstring = "City Council"
            meetingCancelled = item.css(".RowTop div:nth-child(3) span::text").get()
            if (titleSubstring in title) and (not meetingCancelled):
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
        title = item.css(".RowBottom .RowDetails::text").get()
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        dt_obj = item.css(".RowTop .RowLink a::text").get()
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
            "address": "400 N. Douty St. Hanford, CA 93230",
            "name": "Council Chambers",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "hrefAgenda": "http://hanfordca.iqm2.com/Citizens/"
                + item.css(
                    ".RowTop .MeetingLinks div:nth-child(1) a::attr(href)"
                ).get(),
                "titleAgenda": "Agenda",
                "hrefAgendaPacket": "http://hanfordca.iqm2.com/Citizens/"
                + item.css(
                    ".RowTop .MeetingLinks div:nth-child(2) a::attr(href)"
                ).get(),
                "titleAgendaPacket": "Agenda Packet",
                "hrefMinutes": "http://hanfordca.iqm2.com/Citizens/"
                + item.css(
                    ".RowTop .MeetingLinks div:nth-child(4) a::attr(href)"
                ).get(),
                "titleMinutes": "Meeting Minutes",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
