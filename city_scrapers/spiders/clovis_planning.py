from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil import parser


class ClovisPlanningSpider(CityScrapersSpider):
    name = "fre_clovis_planning"
    agency = "Clovis Planning Commission"
    timezone = "America/Los_Angeles"
    start_urls = [
        "https://meetings.municode.com/PublishPage?cid=CLOVIS&"
        "ppid=ad6551de-2ee0-4b3f-b2ab-803f5aca27c8&p=1"
    ]

    def parse(self, response):
        for item in response.css("tr"):
            try:
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
            except AttributeError:
                # there are rows without meeting elements we can skip
                pass

    def _parse_title(self, item):
        return item.css("td.meeting::text").get().strip()

    def _parse_description(self, item):
        return ""

    def _parse_classification(self, item):
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        date = item.css("td.meeting::text").get().strip().split("Planning")[0]
        time = item.css("td.time::text").get().strip()
        datetime = date + time
        return parser.parse(datetime)

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
        return {
            "address": item.css("td.venue::text").get().strip(),
            "name": "",
        }

    def _parse_links(self, item):
        links = []
        for name in ("Agenda", "Packet", "Minutes"):
            link = item.css(f"td.{name.lower()} a::attr(href)").get()
            if link:
                links.append({"href": link, "title": name})
        return links

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
