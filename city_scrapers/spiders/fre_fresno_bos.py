from collections import defaultdict
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider


class FreFresnoBosSpider(LegistarSpider):
    name = "fre_fresno_bos"
    agency = "Fresno County Board of Supervisors"
    timezone = "America/Los_Angeles"
    start_urls = ["https://fresnocounty.legistar.com/Calendar.aspx"]
    # Add the titles of any links not included in the scraped results
    link_types = []

    def _parse_legistar_events(self, response):
        """Override the parent method to fix filtering that requires iCalendar URLs"""
        print(f"Processing URL: {response.url}")
        
        list_view_tab = response.css('#ctl00_ContentPlaceHolder1_tabCalendar_tabStrip .rtsLI')
        if list_view_tab:
            print("Found tab navigation, checking if we need to switch to list view")
            
            selected_tab = response.css('#ctl00_ContentPlaceHolder1_tabCalendar_tabStrip .rtsSelected')
            if selected_tab and 'ListView' not in selected_tab.css('::text').get(''):
                return []

        # Extract events from the table
        events_table = response.css("table.rgMasterTable")
        if not events_table:
            return []
        
        events_table = events_table[0]
        
        # Extract headers
        headers = []
        for header in events_table.css("th[class^='rgHeader']"):
            header_text = (
                " ".join(header.css("*::text").extract()).replace("&nbsp;", " ").strip()
            )
            header_inputs = header.css("input")
            if header_text:
                headers.append(header_text)
            elif len(header_inputs) > 0:
                headers.append(header_inputs[0].attrib["value"])
            else:
                try:
                    headers.append(header.css("img")[0].attrib["alt"])
                except IndexError:
                    headers.append("")
        
        events = []
        rows = events_table.css("tr.rgRow, tr.rgAltRow")
        print(f"Found {len(rows)} event rows")
        
        for row_idx, row in enumerate(rows):
            try:
                data = defaultdict(lambda: None)
                
                # Process each cell in the row
                for header, field in zip(headers, row.css("td")):
                    field_text = (
                        " ".join(field.css("*::text").extract())
                        .replace("&nbsp;", " ")
                        .strip()
                    )
                    url = None
                    if len(field.css("a")) > 0:
                        link_el = field.css("a")[0]
                        if "onclick" in link_el.attrib and link_el.attrib[
                            "onclick"
                        ].startswith(("radopen('", "window.open", "OpenTelerikWindow")):
                            url = response.urljoin(
                                link_el.attrib["onclick"].split("'")[1]
                            )
                        elif "href" in link_el.attrib:
                            url = response.urljoin(link_el.attrib["href"])
                    
                    # Special handling for iCalendar links
                    if url and ("View.ashx?M=IC" in url):
                        print(f"Found iCalendar URL in row {row_idx+1}: {url}")
                        data["iCalendar"] = {"url": url}
                    elif url:
                        value = {"label": field_text, "url": url}
                        data[header] = value
                    else:
                        data[header] = field_text

                # Also add a "Name" field to maintain compatibility with base LegistarSpider
                if "Meeting Body" in data and data["Meeting Body"]:
                    data["Name"] = data["Meeting Body"]
                
                # Include all events with meaningful data
                if data and "Meeting Body" in data:
                    events.append(dict(data))
                    meeting_body = data.get('Meeting Body')
                    if isinstance(meeting_body, dict):
                        meeting_body = meeting_body.get('label', 'Unknown')
                    date = data.get('Meeting Date', 'Unknown date')
                    print(f"Added event: {meeting_body} on {date}")
                elif data:
                    print(f"Found data but missing Meeting Body: {data.keys()}")
            except Exception as e:
                print(f"Error processing row {row_idx+1}: {str(e)}")
        
        print(f"Extracted {len(events)} events")
        return events

    def parse_legistar(self, events):
        """
        `parse_legistar` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        event_list = list(events)
        print(f"Processing {len(event_list)} events from Legistar")
        
        for event in event_list:
            try:
                # Check for the Meeting Body field (Fresno's version of "Name")
                if "Meeting Body" in event:
                    title_field = event["Meeting Body"]
                elif "Name" in event:
                    title_field = event["Name"]
                else:
                    print(f"Warning: Could not find title field in event: {event.keys()}")
                    continue
                
                if isinstance(title_field, dict):
                    title = title_field.get("label", "")
                else:
                    title = title_field
                    
                start = self.legistar_start(event)
                if not start:
                    print(f"Warning: Could not parse start time for event: {title}")
                    continue
                
                meeting = Meeting(
                    title=title,
                    description=self._parse_description(event),
                    classification=self._parse_classification(event),
                    start=start,
                    end=self._parse_end(event),
                    all_day=self._parse_all_day(event),
                    time_notes=self._parse_time_notes(event),
                    location=self._parse_location(event),
                    links=self.legistar_links(event),
                    source=self.legistar_source(event),
                )

                meeting["status"] = self._get_status(meeting)
                meeting["id"] = self._get_id(meeting)
                
                print(f"Yielding meeting: {meeting.get('title')} with ID {meeting.get('id')}")
                yield meeting
                
            except Exception as e:
                print(f"Error creating meeting: {str(e)}")
                import traceback
                print(traceback.format_exc())

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

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
            "address": "2281 Tulare St, Fresno, CA 93724",
            "name": "Hall of Records",
        }
