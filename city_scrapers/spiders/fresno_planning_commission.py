from dateutil import parser
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class FresnoPlanningCommissionSpider(CityScrapersSpider):
    name = "fresno_planning_commission"
    agency = "Fresno County Planning Commission"
    timezone = "America/Los_Angeles"
    start_urls = ["https://www.co.fresno.ca.us/departments/public-works-planning/divisions-of-public-works-and-planning/development-services-division/planning-and-land-use/planning-commission/plann/-toggle-allupcoming"]

    def parse(self, response):
        for item in response.css("table tbody tr"):
            meeting = Meeting(
                title=self._parse_title(item),
                description="",
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes="",
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return item.xpath(".//span[@itemprop='summary']/text()").get()

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        return parser.parse(item.xpath(".//time[@itemprop='startDate']/text()").get())

    def _parse_end(self, item):
        return parser.parse(item.xpath(".//time[@itemprop='endDate']/text()").get())

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        href = item.xpath(".//a[@itemprop='url']/@href").get()
        title = item.xpath(".//span[@itemprop='summary']/text()").get()
        return [{"href": href, "title": title}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
