import re
from io import StringIO
from urllib import request

from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


class FreChowchillaCityCouncilSpider(CityScrapersSpider):
    name = "fre_chowchilla_city_council"
    agency = "Chowchilla City Council"
    timezone = "America/Chicago"
    start_urls = ["https://www.cityofchowchilla.org/agendacenter"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("table[id='table2'] tr")[1:]:
            title = item.css("td:nth-child(1) p a::text").get()
            if ("City Council" in title) and ("Closed" not in title):
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
        title = item.css("td:nth-child(1) p a::text").get()
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""

        # meeting time noted on Agenda PDF
        # download Agenda PDF, extract start time, delete Agenda PDF
        agendaPDF = (
            "https://www.cityofchowchilla.org"
            + item.css("td:nth-child(1) p a::attr(href)").get()
        )
        request.urlretrieve(agendaPDF, "pdf")
        resource_manager = PDFResourceManager(caching=True)
        out_text = StringIO()
        laParams = LAParams()
        text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
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

        # some meetings have specific Open Session for the public
        # if the agenda indicates an open session time, find open session time
        try:
            timeTextOpen = re.findall(r"Open Session: \d{1,2}:\d{1,2} .", text)[0]
        except IndexError:
            timeTextOpen = ""
        # meeting has no open session, use whatever time shows up on agenda first
        timeText = re.findall(r"\d{1,2}:\d{1,2} .", text)[0]
        fp.close()
        text_converter.close()
        out_text.close()

        if timeTextOpen:
            time = timeTextOpen.split(" ", 2)[2]
        else:
            time = timeText

        # get date of meeting
        date_raw = item.css("td:nth-child(1) h4 strong::attr(aria-label)").get()
        date = date_raw.split(" ", 2)[2]

        # combine date and time
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
            "address": "Chowchilla City Hall 130 S. Second Street, Chowchilla, CA 93610",  # noqa
            "name": "Council Chambers",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "href": "https://www.cityofchowchilla.org"
                + item.css("td:nth-child(1) p a::attr(href)").get(),
                "title": "Agenda",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
