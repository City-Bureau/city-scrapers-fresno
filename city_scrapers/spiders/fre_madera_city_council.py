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


class FreMaderaCityCouncilSpider(CityScrapersSpider):
    name = "fre_madera_city_council"
    agency = "Madera City Council"
    timezone = "America/Chicago"
    start_urls = [
        "https://www.madera.gov/home/departments/city-clerk/city-council-agendas-meetings/#tr-2022-meetings-4850011" # noqa
    ]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("table[id='tablepress-49'] tr")[1:]:
            meetingType = item.css("td:nth-child(4)::text").get()
            substring = "LD"
            if substring not in meetingType:
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
        meetingType = item.css("td:nth-child(4)::text").get()
        title = ""

        if "RM" in meetingType:
            title = "Regular Meeting of the Madera City Council"
        if "SM" in meetingType:
            title = "Special Meeting of the Madera City Council"

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
        agendaPDF = item.css("td:nth-child(2) a::attr(href)").get()
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
        time = re.findall(r"\d{1,2}:\d{1,2} ....", text)[0]
        fp.close()
        text_converter.close()
        out_text.close()

        date = item.css("td:nth-child(1)::text").get()
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
            "address": "205 W. 4th Street, Madera, California 93637",
            "name": "Council Chambers, City Hall",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [
            {
                "hrefAgenda": item.css("td:nth-child(2) a::attr(href)").get(),
                "titleAgenda": "Agenda",
                "hrefReport": item.css("td:nth-child(3) a::attr(href)").get(),
                "titleReport": "Report",
                "hrefVideo": item.css("td:nth-child(6) a::attr(href)").get(),
                "titleVideo": "Video",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
