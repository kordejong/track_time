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
    records = []
    pattern = re.compile(r"(?P<date>[0-9]{8})\s*:\s*(?P<nrHours>[0-9]+)")
    for line in stream:
      # Split at the comment sign. The stuff before the sign is relevant.
      line = line.split("#")[0].strip()
      if len(line) == 0:
        continue

      # <date/time>: <nr hours> | <period>+: project
      match = re.match(pattern, line)

      if match is None:
        raise Exception("bla")

      assert(not match.group("date") is None)
      assert(not match.group("nrHours") is None)

      date = match.group("date")
      date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))
      records.append(TrackTime.Record(date=date,
        nrHours=int(match.group("nrHours"))))

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

