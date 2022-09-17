from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class FreKingsBosSpider(CityScrapersSpider):
    name = "fre_kings_bos"
    agency = "Kings County Board of Supervisors"
    timezone = "America/Chicago"
    start_urls = ["https://www.countyofkings.com/community/calendar-of-events"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("td.calendar_day_with_items"):
            title = item.css(
                "div.calendar_items div.calendar_item a::attr(title)"
            ).get()
            if ("Board of Supervisors" in title) and ("Canceled" not in title):
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
        title = item.css("div.calendar_items div.calendar_item a::attr(title)").get()
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return "Check meeting link for meeting details and agenda"

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        startDate = item.css("::attr(aria-label)").get()
        startTime = item.css(
            "div.calendar_items div.calendar_item span.calendar_eventtime::text"
        ).get()
        dt_obj = startDate + " " + startTime
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
            "address": "1400 W. Lacey Boulevard, Hanford, California 93230",
            "name": "Board of Supervisors Chambers, Kings County Government Center",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "href": "https://www.countyofkings.com"
                + item.css("div.calendar_items div.calendar_item a::attr(href)").get(),
                "title": "Meeting Details",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
