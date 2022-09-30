import requests
import re
from dateutil import parser
from pdfminer.high_level import extract_text
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class FreMendotaCityCouncilSpider(CityScrapersSpider):
    name = "fre_mendota_city_council"
    agency = "Mendota City Council"
    timezone = "America/Chicago"
    start_urls = ["https://www.ci.mendota.ca.us/agendas-and-minutes/"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """

        # first tab is current year, each tab has 3 columns
        date_tab, link_tab1, link_tab2 = response.css(".wpb_tab")[0].css(
            ".vc_column-inner"
        )

        # data is grouped by column, use zip to regroup the three
        dates = date_tab.css("p::text").getall()
        links1 = link_tab1.css("p")
        links2 = link_tab2.css("p")

        for date, link1p, link2p in zip(dates, links1, links2):
            links = []
            link1href = link1p.css("a::attr(href)").get()
            link1name = link1p.css("a::text").get()
            link2href = link2p.css("a::attr(href)").get()
            link2name = link2p.css("a::text").get()

            if link1href:
                links.append({"href": link1href, "title": link1name})
            if link2href:
                links.append({"href": link2href, "title": link2name})

            time = self._extract_time(link1href)
            parsed_date = parser.parse(date + " " + time)

            meeting = Meeting(
                title=date,
                description="",
                classification=NOT_CLASSIFIED,
                start=parsed_date,
                end=None,
                all_day=False,
                time_notes="",
                links=links,
                location=self._parse_location(None),
                source=self._parse_source(response),
            )
            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)
            yield meeting

    def _extract_time(self, pdflink):
        print("PDF", pdflink)
        with open("pdf", "wb") as f:
            f.write(
                requests.get(
                    pdflink,
                    headers={
                        "User-agent": "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"  # noqa
                    },
                ).content
            )
        text = extract_text("pdf")
        for line in text:
            time = re.findall(r"\d{1,2}:\d{2} [AP]M", line)
            if time:
                return time[0]
        return ""

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
