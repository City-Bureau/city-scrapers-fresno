import datetime
import re
from io import StringIO

import requests
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


class FreReedleyCityCouncilSpider(CityScrapersSpider):
    name = "fre_reedley_city_council"
    agency = "Reedley City Council"
    timezone = "America/Los_Angeles"
    start_urls = ["https://reedley.ca.gov/city-council/city-council-agendas/"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(
            "div[id='content_9fa5f83a70fceefbd52c6d537bd704cc'] div.row"
        ):
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

        title = item.css(
            "div div div div div:nth-child(2) h3.media-heading a::text"
        ).get()
        if "Special Meeting" in title:
            title = "Special Meeting"
        else:
            title = "Regular Meeting"

        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return CITY_COUNCIL

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        startTime = "00:00"

        # meeting time noted on Agenda PDF
        # download Agenda PDF, extract start time, delete Agenda PDF
        # if agenda is not scrapable assume 7PM meeting time
        agendaPDF = item.css(
            "div div div div div:nth-child(2) h3.media-heading a::attr(href)"
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
            time = re.findall(r"\d{1,2}:\d{1,2} [AP].M.", text)
            if time:
                startTime = time[0]
            fp.close()
            text_converter.close()
            out_text.close()
        else:
            startTime = "19:00:00"

        dateRaw = item.css(
            "div div div div div:nth-child(2) h3.media-heading a::text"
        ).get()
        startDate = dateRaw.split("-")[0] + " " + str((datetime.date.today()).year)

        dt_obj = startDate + " " + startTime
        return parser().parse(dt_obj)

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        # meeting time noted on Agenda PDF
        # if agenda is not scrapable assume 7PM meeting time and notify user to check the agenda link  # noqa
        agendaPDF = item.css(
            "div div div div div:nth-child(2) h3.media-heading a::attr(href)"
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
            time = re.findall(r"\d{1,2}:\d{1,2} [AP].M.", text)
            if not time:
                timeNote = "Time is unscrapable from agenda and is assumed to be 7PM, check agenda link to verify."  # noqa
            else:
                timeNote = ""
            fp.close()
            text_converter.close()
            out_text.close()

        return timeNote

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "845 'G' Street, Reedley, California ",
            "name": "Council Chambers",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "href": item.css("div div div div:nth-child(2) h3 a::attr(href)").get(),
                "title": "Agenda",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
