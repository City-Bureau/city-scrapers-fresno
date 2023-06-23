import re
from io import StringIO

import requests
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


class FreMaderaIrrigationDistrictSpider(CityScrapersSpider):
    name = "fre_madera_irrigation_district"
    agency = "Madera Irrigation District"
    timezone = "America/Los_Angeles"
    start_urls = [
        "https://www.madera-id.org/governance/agendas-and-minutes/2022-agendas-and-minutes/"  # noqa
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(
            "main.main-2022-agendas-and-minutes div.container table tr"
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

        # some rows have multiple links on the left side of the same row
        # need to check if any of the links are agendas or notices of cancellation

        # by default, the title assumes there are no agendas, only a notice of cancellation.  # noqa
        title = "NO MEETING - CHECK CANCELLATION NOTICE"
        array = []

        # collect links in an array
        # check if any of the links are agendas
        # if there is a meeting agenda, return the meeting title
        # if there is a notice of cancellation, indicate meeting is cancelled.
        array = item.css("td:nth-child(2) ul li a::text").getall()
        for item in array:
            if "Agenda" in item:
                title = item

        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""

        # if there's no meeting, tell user to check meeting cancellation notice.

        descriptiption = ""
        title = "NO MEETING - CHECK CANCELLATION NOTICE"
        array = []

        array = item.css("td:nth-child(2) ul li a::text").getall()
        for item in array:
            if "Agenda" in item:
                title = item

        if "NO MEETING" in title:
            descriptiption = "Meeting cancelled, check notice link."

        return descriptiption

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        startDate = item.css("td:nth-child(1)::text").get()
        startTime = ""
        array = []
        index = 0

        # links for a specific date are on the left side of each row
        # collect links for a row in an array
        # check for the link that's the agenda
        # note down the agenda link's position in the array
        # the <li> element that contains the agenda's link is the nth <li> element where n = array position plus 1 (becasue arrays start at 0 instead of 1)  # noqa

        array = item.css("td:nth-child(2) ul li a::text").getall()
        for row in array:
            if "Agenda" in row:
                index = array.index(row) + 1

        # meeting time noted on Agenda PDF
        # download Agenda PDF, extract start time, delete Agenda PDF

        agendaPDF = item.css(
            "td:nth-child(2) ul li:nth-child(" + str(index) + ") a::attr(href)"
        ).get()
        if agendaPDF:
            with open("pdf", "wb") as fp:
                resp = requests.get(
                    agendaPDF,
                    headers={
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)"
                    },
                )
                resp.raise_for_status()
                fp.write(resp.content)
            resource_manager = PDFResourceManager(caching=True)
            out_text = StringIO()
            laParams = LAParams()
            text_converter = TextConverter(
                resource_manager, out_text, laparams=laParams
            )
            fp = open("pdf", "rb")
            interpreter = PDFPageInterpreter(resource_manager, text_converter)
            for page in PDFPage.get_pages(
                fp,
                pagenos=set(),
                maxpages=1,
                password="",
                caching=True,
                check_extractable=True,
            ):
                interpreter.process_page(page)
            text = out_text.getvalue()
            time = re.findall(r"\d{1,2}:\d{1,2} [ap].m.", text)
            if time:
                startTime = time[0]
            fp.close()
            text_converter.close()
            out_text.close()

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
            "address": "12152 Road 28 ¼, Madera, California 93637",
            "name": "Madera Irrigation District",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        array = []
        index = 0

        # links for a specific date are on the left side of each row
        # collect links for a row in an array
        # check for the link that's the agenda or notice of cancellation
        # note down the link's position in the array
        # the <li> element that contains the link is the nth <li> element where n = array position plus 1 (becasue arrays start at 0 instead of 1)  # noqa

        array = item.css("td:nth-child(2) ul li a::text").getall()
        for row in array:
            if "Agenda" in row:
                index = array.index(row) + 1
            if "Cancellation" in row:
                index = array.index(row) + 1

        agendaLink = item.css(
            "td:nth-child(2) ul li:nth-child(" + str(index) + ") a::attr(href)"
        ).get()

        return [{"href": agendaLink, "title": "Meeting Link"}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
