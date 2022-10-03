from datetime import datetime
from pdfminer.high_level import extract_text
from city_scrapers_core.constants import (CITY_COUNCIL, 
                                          COMMISSION, 
                                          NOT_CLASSIFIED)
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class FreFowlerCityCouncilSpider(CityScrapersSpider):
    name = "fre_fowler_city_council"
    agency = "Fowler City Council"
    timezone = "America/Los_Angeles"
    start_urls = ["https://fowlercity.org/agendas-minutes/"]
    cur_year = datetime.now().year

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        data_attr = "::attr(data-title)"
        meeting_tab_sel_str = "div.su-tabs-pane"
        meeting_tab_sel_list = response.css(meeting_tab_sel_str)

        for meeting_tab in meeting_tab_sel_list:
            if str(self.cur_year) in meeting_tab.css(data_attr).get():
                meeting_tab_title = meeting_tab.css(data_attr).get().strip()
                for item in meeting_tab.css('div p'):
                    meeting = Meeting(
                        title=self._parse_title(item, meeting_tab_title),
                        description=self._parse_description(item),
                        classification=self._parse_classification(item, 
                                                        meeting_tab_title),
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

    def _parse_title(self, item, meeting_tab_title=None):
        """Parse or generate meeting title."""
        title = ""
        if meeting_tab_title:
            title += meeting_tab_title + ": "
        title += item.css("::text").get().strip(" —")
        return title if title else ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item, meeting_tab_title=None):
        """Parse or generate classification from allowed options."""
        if meeting_tab_title:
            if "COUNCIL" in meeting_tab_title.upper():
                return CITY_COUNCIL
            elif "COMMISSION" in meeting_tab_title.upper():
                return COMMISSION
        else:
            return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        title_list = item.css("::text").get().strip(" —").split()
        try: 
            month = title_list[0].strip()
            day = int(title_list[1].strip(','))
            year = int(title_list[2].strip())
            return datetime.strptime(f"{year:04}-{month}-{day:02} 19:00",
                                     "%Y-%B-%d %H:%M")
        except Exception:
            return datetime(1, 1, 1, 0, 0)

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ("Meetings regularly take place at 7:00 PM PST, "
                "but are subject to change. Refer to agenda if available.")

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {"address" : "128 SOUTH 5TH STREET FOWLER, CA 93625",
                "name" : "CITY COUNCIL CHAMBER"}

    def _parse_links(self, item):
        """Parse or generate links."""
        link_list = []
        for link_sel in item.css("p a"):
            link = link_sel.css("::attr(href)").get()
            title = link.split("/")[len(link.split("/"))-1][:-4]
            link_list.append({ "href" : link, "title": title })
        return link_list

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
