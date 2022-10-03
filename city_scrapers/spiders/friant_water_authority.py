from datetime import datetime

from city_scrapers_core.constants import BOARD, COMMITTEE, NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class FriantWaterAuthoritySpider(CityScrapersSpider):
    name = "fre_friant_water_authority"
    agency = "Friant Water Authority"
    timezone = "America/Los_Angeles"
    start_urls = ["https://friantwater.org/meetings-events"]

    def parse(self, response):
        """
        Parse the Meeting Events of the Friant Water Authority site
        """
        for item in response.css(".eventlist-column-info"):
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
        title = item.css(".eventlist-title-link::text").get().strip()
        return title if title else ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        title = self._parse_title(item)
        if "BM" in title.upper() or "BOARD" in title.upper():
            return BOARD
        elif "COMMITTEE" in title.upper():
            return COMMITTEE
        else:
            return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        start_sel = item.css("span.event-time-24hr time.event-time-24hr-start")
        start_date = start_sel.attrib["datetime"]
        start_time = start_sel.css("::text").get()
        datetime_str = f"{start_date} {start_time}"
        start = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        return start

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        end_sel = item.css("span.event-time-24hr time.event-time-12hr-end")
        end_date = end_sel.attrib["datetime"]
        end_time = end_sel.css("::text").get()
        datetime_str = f"{end_date} {end_time}"
        end = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        return end

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        location_dict = {}
        google_maps_prefix = "http://maps.google.com?q="
        map_sel_str = (
            ".eventlist-meta-item" ".eventlist-meta-address" ".event-meta-item"
        )

        for map_sel in item.css(map_sel_str):
            map_title = map_sel.css("::text").get().strip("\n ")
            map_link_sel = ".eventlist-meta-address-maplink::attr(href)"
            map_link = map_sel.css(map_link_sel).get()
            address = map_link.removeprefix(google_maps_prefix)
            location_dict["address"] = address.strip()
            location_dict["name"] = map_title.strip()

        return location_dict

    def _parse_links(self, item):
        """Parse or generate links."""
        link_list = []
        link_sel_str = ".sqs-block-button-element::attr(href)"

        # Parsing for attachments
        for link in item.css(link_sel_str).getall():
            title = link.split("/")[len(link.split("/")) - 1].split(".")[0]
            link_list.append({"href": link, "title": title})

        # Parsing for Google Maps links
        map_sel_str = (
            ".eventlist-meta-item" ".eventlist-meta-address" ".event-meta-item"
        )

        for map_sel in item.css(map_sel_str):
            map_title = map_sel.css("::text").get().strip("\n ") + " Map Link"
            map_link_sel = ".eventlist-meta-address-maplink::attr(href)"
            map_link = map_sel.css(map_link_sel).get()
            link_list.append({"href": map_link, "title": map_title})

        return link_list

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
