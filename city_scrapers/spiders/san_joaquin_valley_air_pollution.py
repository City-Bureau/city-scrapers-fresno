from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parser


class SanJoaquinValleyAirPollutionSpider(CityScrapersSpider):
    name = "fre_san_joaquin_valley_air_pollution"
    agency = "San Joaquin Valley Air Pollution Control District"
    timezone = "America/Chicago"
    start_urls = ["https://www.valleyair.org/Board_meetings/GB/GB_meetings_2022.htm"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(".text-med .text-med tr"):
            agenda = item.css("td:nth-child(2) a::attr(href)").get()
            if agenda:
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
        return (
            "San Joaquin Valley Unified Air Pollution Control District Governing Board"
        )

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        date = item.css("td:nth-child(1)::text").get()
        time = "9:00"
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
            "address": "1990 E. Gettysburg Avenue, Fresno, CA",
            "name": "Central Region Office, Governing Board Room",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        agenda = ""
        minutes = ""
        presentations = ""
        recording = ""

        agendaRaw = item.css("td:nth-child(2) a::attr(href)").get()
        minutesRaw = item.css("td:nth-child(3) a::attr(href)").get()
        presentationsRaw = item.css("td:nth-child(4) a::attr(href)").get()
        recordingRaw = item.css("td:nth-child(5) a::attr(href)").get()

        if agendaRaw:
            agenda = "https://www.valleyair.org/Board_meetings/GB/" + agendaRaw

        if minutesRaw:
            minutes = "https://www.valleyair.org/Board_meetings/GB/" + minutesRaw

        if presentationsRaw:
            presentations = (
                "https://www.valleyair.org/Board_meetings/GB/" + presentationsRaw
            )

        if recordingRaw:
            recording = recordingRaw

        return [
            {
                "hrefAgenda": agenda,
                "titleAgenda": "Agenda",
                "hrefMinutes": minutes,
                "titleMinutes": "Minutes",
                "hrefPresentations": presentations,
                "titlePresentations": "Presentations",
                "hrefRecording": recording,
                "titleRecording": "Recording",
            }
        ]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
