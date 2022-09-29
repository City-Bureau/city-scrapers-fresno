from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class FreMeasureCCommitteeSpider(CityScrapersSpider):
    name = "fre_measure_c_committee"
    agency = "Measure C Committee"
    timezone = "America/Chicago"
    start_urls = ["https://measurec.com/meetings/"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("div.vc_custom_1642124059800 ul li"):
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

        title = "Committee Meeting"
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        startTime = "09:00:00"
        startDate = ""

        if item.css("::text").get():
            date = item.css("::text").get()
            startDate = (
                date.split(" ", 4)[1]
                + " "
                + date.split(" ", 4)[2]
                + " "
                + date.split(" ", 4)[3]
            )

        if item.css("strong::text").get():
            date = item.css("strong::text").get()
            startDate = (
                date.split(" ", 4)[1]
                + " "
                + date.split(" ", 4)[2]
                + " "
                + date.split(" ", 4)[3]
            )

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
        # if "Ash Conference Room" in description:
        name = "Fresno Council of Government’s Ash Conference Room"
        address = "2035 Tulare Street, Suite 201, 2nd Floor, Fresno, California"

        return {
            "address": address,
            "name": name,
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
