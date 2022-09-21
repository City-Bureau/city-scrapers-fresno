from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class SanJoaquinRiverConservancySpider(CityScrapersSpider):
    name = "san_joaquin_river_conservancy"
    agency = "San Joaquin River Conservancy"
    timezone = "America/Chicago"
    start_urls = ["http://sjrc.ca.gov/Board/"]

    def parse(self, response):
        """
        Main parse method for the San Joaquin River Conservancy
        Yields Meeting objects
        """
        td_sel_str = 'td[style="text-align: center;"][align="left"]'
        td_response = response.css(td_sel_str)
        td_sel_list = td_response.css("*")[1::]

        # Dictionary to store board meeting information
        # Keys: Title (str)
        # Values: Selection Objects
        board_meeting_dict = {}

        # Parsing the td element sequentially
        cur_meeting = None
        for sel in td_sel_list:
            title = sel.css("::text").get()
            if sel.css("p strong") and "Board Meeting" in title:
                cur_meeting = title
                board_meeting_dict[cur_meeting] = []
            if sel.css("h3"):
                cur_meeting = None
            if cur_meeting is not None and sel.css("a"):
                board_meeting_dict[cur_meeting].append(sel)

        for title, sel_list in board_meeting_dict.items():
            item = (title, sel_list)
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
        return item[0] if item else ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        date_str_list = item[0].split("-")[0].split()
        month = datetime.strptime(date_str_list[0].strip(), "%B").month
        day = date_str_list[1].strip()

        # Meetings start at 10:00 AM between March and October
        # Otherwise, meeting start at 10:30 AM
        if int(month) >= 3 and int(month) <= 10:
            meeting_time = "10:00:00"
        else:
            meeting_time = "10:30:00"

        # Parsing the current year from the agenda link
        # Defaults to current year if parsing fails
        year = datetime.now().year
        agenda_header = "http://sjrc.ca.gov/wp-content/uploads/"
        for sel in item[1]:
            agenda_link = sel.css("::attr(href)").get()
            if agenda_header in agenda_link:
                year = agenda_link[len(agenda_header) : len(agenda_header) + 4]
        start = f"{year} {int(month):02} {int(day):02} {meeting_time}"

        return datetime.strptime(start, "%Y %m %d %H:%M:%S")

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        time_notes_str = (
            "Scheduled meetings are subject to change. "
            "Refer to Agenda if available. For more information "
            "email info@sjrc.ca.gov or call (559) 253-7324."
        )
        return time_notes_str

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "5469 E. Olive Ave., Fresno, CA 93727",
            "name": "Fresno Metropolitan Flood Control District Board Room",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        link_dict = {}
        for sel in item[1]:
            link = sel.css("::attr(href)").get()
            title = link.split("/")[len(link.split("/")) - 1].split(".")[0]
            link_dict[link] = title
        return link_dict

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
