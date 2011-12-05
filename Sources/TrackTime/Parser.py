# -*- coding: utf-8 -*-
"""
Parser
******
"""
import datetime
import re
import TrackTime.Record



class Parser(object):
  """
  Parser for parsing files with information about time periods worked on
  projects.
  """

  def __init__(self):
    pass

  def parse(self,
    stream):
    """
    Parse `stream` for records with information about hours spent working per
    day and project.

    Return list of TrackTime.Record instances.
    """
    def dateTime(
      date,
      tokens):
      assert(len(tokens) == 2)
      nrHours = int(tokens[0])
      assert(0 <= nrHours <= 24)
      nrMinutes = int(tokens[1])
      assert(0 <= nrMinutes <= 60)
      return datetime.datetime(date.year, date.month, date.day, nrHours,
        nrMinutes)

    records = {}
    periodPattern = r"\d{1,2}:\d{2}-\d{1,2}:\d{2}"
    pattern = r"""
      (?P<date>\d{8})
      \s*:\s*
      ((?P<periods>periodPattern(\s*,\s* periodPattern)*) |
        (?P<nrHours>\d{1,2}(\.\d{1,2})?))
    """
    pattern = pattern.replace("periodPattern", periodPattern)
    pattern = re.compile(pattern, re.VERBOSE)
    for line in stream:
      # Split at the comment sign. The stuff before the sign is relevant.
      line = line.split("#")[0].strip()
      if len(line) == 0:
        continue

      match = re.match(pattern, line)

      if match is None:
        raise Exception("Parse error: {0}".format(line))
      elif match.end() != len(line):
        raise Exception("Parse error at character {0}: {1}".format(
          match.end() + 1, line))

      assert(not match.group("date") is None)
      assert(match.group("nrHours") or match.group("periods"))
      assert(not (match.group("nrHours") and match.group("periods")))

      date = match.group("date")
      date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))

      if not date in records:
        records[date] = []
      if match.group("nrHours"):
        records[date].append(TrackTime.Record(date=date,
          nrHours=float(match.group("nrHours"))))
      else:
        nrHours = 0
        # "9:30-12:00, 12:30-17:00" -> ["9:30-12:00", "12:30-17:00"]
        periodStrings = [periodString.strip() for periodString in \
          match.group("periods").split(",")]
        for periodString in periodStrings:
          # "9:30-12:00" -> ["9:30", "12:00"]
          timeStrings = [timeString.strip() for timeString in \
            periodString.split("-")]
          assert(len(timeStrings) == 2)

          # "9:30" -> ["9", "30"]
          tokens = timeStrings[0].split(":")

          startTime = dateTime(date, timeStrings[0].split(":"))
          endTime = dateTime(date, timeStrings[1].split(":"))
          assert(endTime >= startTime)
          period = endTime - startTime
          nrHours += period.total_seconds() / 60.0 / 60.0

        records[date].append(TrackTime.Record(date=date, nrHours=nrHours))

      ### if record.find(":") == -1:
      ###   # Number of hours not entered. Assume 8 hours.
      ###   date = stringToDate(record)
      ###   hours[date] = 8.0
      ### else:
      ###   dateString, periodStrings = record.split(":", 1)
      ###   date = stringToDate(dateString)
      ###   hours[date] = []

      ###   periodStrings = map(lambda period: period.strip().split("-"),
      ###         periodStrings.split(","))

      ###   nrHoursWorked = 0

      ###   for periodString in periodStrings:
      ###     assert len(periodString) == 1 or len(periodString) == 2, periodString
      ###     if len(periodString) == 1:
      ###       # Allow a total number of hours to be input, instead of a period.
      ###       nrHoursWorked = float(periodString[0])
      ###     else:
      ###       # Figure out the amount of time between end time and start time of
      ###       # period worked.
      ###       startTime = stringToTime(date, periodString[0])
      ###       endTime = stringToTime(date, periodString[1])
      ###       nrHoursWorked += (endTime - startTime).seconds / 3600.0

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
###         dateString, periodStrings = record.split(":", 1)
###         date = stringToDate(dateString)
###         hours[date] = []
### 
###         periodStrings = map(lambda period: period.strip().split("-"),
###               periodStrings.split(","))
### 
###         nrHoursWorked = 0
### 
###         for periodString in periodStrings:
###           assert len(periodString) == 1 or len(periodString) == 2, periodString
###           if len(periodString) == 1:
###             # Allow a total number of hours to be input, instead of a period.
###             nrHoursWorked = float(periodString[0])
###           else:
###             # Figure out the amount of time between end time and start time of
###             # period worked.
###             startTime = stringToTime(date, periodString[0])
###             endTime = stringToTime(date, periodString[1])
###             nrHoursWorked += (endTime - startTime).seconds / 3600.0
### 
###         hours[date] = nrHoursWorked
### 
###     return hours

