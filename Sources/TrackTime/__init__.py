# -*- coding: utf-8 -*-
"""
*********
TrackTime
*********
The TrackTime package contains code needed for tracking time periods worked
on projects.

.. automodule:: TrackTime.Record
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: TrackTime.Aggregator
   :members:
   :undoc-members:
   :show-inheritance:

"""
import datetime
import re
import TrackTime.Record
from TrackTime.Aggregator import Aggregator
from TrackTime.Record import Record


def parse(
        stream):
    """
    Parse `stream` for records with information about hours spent working,
    sick, holidaying, or vacationing per day and project.

    Return list of TrackTime.Record instances.
    """
    def date_time(
            date,
            tokens):
        assert(len(tokens) == 2)
        nr_hours = int(tokens[0])
        assert(0 <= nr_hours <= 24)
        nr_minutes = int(tokens[1])
        assert(0 <= nr_minutes <= 60)
        return datetime.datetime(date.year, date.month, date.day, nr_hours,
            nr_minutes)

    records = {}
    period_pattern = r"\d{1,2}:\d{2}-\d{1,2}:\d{2}"
    pattern = r"""
        (?P<date>\d{8})
        (\s*:\s*
        ((?P<periods>period_pattern(\s*,\s* period_pattern)*) |
            (?P<nr_hours>\d{1,2}(\.\d{1,2})?))
        (\s*:\s\s*
        (?P<project>\S+))?)?
    """
    pattern = pattern.replace("period_pattern", period_pattern)
    pattern = re.compile(pattern, re.VERBOSE)
    for line in stream:
        # Split at the comment sign. The stuff before the sign is relevant.
        line = line.split("#")[0].strip()
        if len(line) == 0:
            continue

        match = re.match(pattern, line)

        if match is None:
            raise ValueError("Parse error: {}".format(line))
        elif match.end() != len(line):
            raise ValueError("Parse error at character {}: {}".format(
                match.end() + 1, line))

        assert(not match.group("date") is None)
        # assert(match.group("nr_hours") or match.group("periods"))
        assert(not (match.group("nr_hours") and match.group("periods")))

        date = match.group("date")
        date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))

        if not date in records:
            records[date] = []
        if not match.group("nr_hours") and not match.group("periods"):
            records[date].append(TrackTime.Record(date=date,
                nr_hours=8.0))
        elif match.group("nr_hours"):
            records[date].append(TrackTime.Record(date=date,
                nr_hours=float(match.group("nr_hours")),
                project=match.group("project")))
        else:
            nr_hours = 0
            # "9:30-12:00, 12:30-17:00" -> ["9:30-12:00", "12:30-17:00"]
            period_strings = [period_string.strip() for period_string in \
                match.group("periods").split(",")]
            for period_string in period_strings:
                # "9:30-12:00" -> ["9:30", "12:00"]
                time_strings = [time_string.strip() for time_string in \
                    period_string.split("-")]
                assert(len(time_strings) == 2)

                # "9:30" -> ["9", "30"]
                tokens = time_strings[0].split(":")

                start_time = date_time(date, time_strings[0].split(":"))
                end_time = date_time(date, time_strings[1].split(":"))
                assert(end_time >= start_time)
                period = end_time - start_time
                nr_hours += period.total_seconds() / 60.0 / 60.0

            records[date].append(TrackTime.Record(date=date,
                nr_hours=nr_hours, project=match.group("project")))




      ### if record.find(":") == -1:
      ###   # Number of hours not entered. Assume 8 hours.
      ###   date = stringToDate(record)
      ###   hours[date] = 8.0
      ### else:
      ###   dateString, period_strings = record.split(":", 1)
      ###   date = stringToDate(dateString)
      ###   hours[date] = []

      ###   period_strings = map(lambda period: period.strip().split("-"),
      ###         period_strings.split(","))

      ###   nrHoursWorked = 0

      ###   for period_string in period_strings:
      ###     assert len(period_string) == 1 or len(period_string) == 2, period_string
      ###     if len(period_string) == 1:
      ###       # Allow a total number of hours to be input, instead of a period.
      ###       nrHoursWorked = float(period_string[0])
      ###     else:
      ###       # Figure out the amount of time between end time and start time of
      ###       # period worked.
      ###       start_time = stringToTime(date, period_string[0])
      ###       end_time = stringToTime(date, period_string[1])
      ###       nrHoursWorked += (end_time - start_time).seconds / 3600.0

    return records


###   def _parseHourInformation(self,
###          stream):
### 
###     hours = {}
### 
###     for record in stream:
###       record = record.split("#")[0].strip()
### 
###       if len(record) == 0:
###         # Comment line.
###         continue
### 
###       if record.find(":") == -1:
###         # Number of hours not entered. Assume 8 hours.
###         date = stringToDate(record)
###         hours[date] = 8.0
###       else:
###         dateString, period_strings = record.split(":", 1)
###         date = stringToDate(dateString)
###         hours[date] = []
### 
###         period_strings = map(lambda period: period.strip().split("-"),
###               period_strings.split(","))
### 
###         nrHoursWorked = 0
### 
###         for period_string in period_strings:
###           assert len(period_string) == 1 or len(period_string) == 2, period_string
###           if len(period_string) == 1:
###             # Allow a total number of hours to be input, instead of a period.
###             nrHoursWorked = float(period_string[0])
###           else:
###             # Figure out the amount of time between end time and start time of
###             # period worked.
###             start_time = stringToTime(date, period_string[0])
###             end_time = stringToTime(date, period_string[1])
###             nrHoursWorked += (end_time - start_time).seconds / 3600.0
### 
###         hours[date] = nrHoursWorked
### 
###     return hours
