#!/usr/bin/env python
import datetime
import os.path



def stringToDate(string):
  assert len(string) == 8, string

  year = int(string[0:4])
  month = int(string[4:6])
  day = int(string[6:8])
  return datetime.date(year, month, day)



def stringToTime(date, string):
  parts = map(lambda part: int(part), string.split(":"))

  if len(parts) == 1:
    return datetime.datetime(date.year, date.month, date.day, parts[0])
  else:
    assert len(parts) == 2
    return datetime.datetime(date.year, date.month, date.day, parts[0],
      parts[1])



class TimeTracker(object):

  def __init__(self,
         workedStream,
         vacationStream,
         holidaysStream,
         sickStream,
         contractHoursPerWeek,
         vacationDaysPerYear):

    # Sources of information.
    self.workedStream = workedStream
    self.vacationStream = vacationStream
    self.holidaysStream = holidaysStream
    self.sickStream = sickStream

    # Contract properties.
    self.contractHoursPerWeek = contractHoursPerWeek
    self.vacationDaysPerYear = vacationDaysPerYear

    # Dictionaries with { date: hours }.
    self.worked = self.vacation = self.holidays = self.sick = {}

    # Dictionary with { date: hours }.
    # All hours aggregated per day.
    self.hoursPerDay = {}

    # Dictionary with { week: hours }.
    # All hours aggregated per week.
    self.hoursPerWeek = {}

    # Last week that hours have been entered. It is assumed that the weeks
    # after this week do not contain relevant information yet.
    self.lastWeekEntered = 0

  def _parseHourInformation(self,
         stream):

    hours = {}

    for record in stream:
      record = record.split("#")[0].strip()

      if len(record) == 0:
        # Comment line.
        continue

      if record.find(":") == -1:
        # Number of hours not entered. Assume 8 hours.
        date = stringToDate(record)
        hours[date] = 8.0
      else:
        dateString, periodStrings = record.split(":", 1)
        date = stringToDate(dateString)
        hours[date] = []

        periodStrings = map(lambda period: period.strip().split("-"),
              periodStrings.split(","))

        nrHoursWorked = 0

        for periodString in periodStrings:
          assert len(periodString) == 1 or len(periodString) == 2, periodString
          if len(periodString) == 1:
            # Allow a total number of hours to be input, instead of a period.
            nrHoursWorked = float(periodString[0])
          else:
            # Figure out the amount of time between end time and start time of
            # period worked.
            startTime = stringToTime(date, periodString[0])
            endTime = stringToTime(date, periodString[1])
            nrHoursWorked += (endTime - startTime).seconds / 3600.0

        hours[date] = nrHoursWorked

    return hours

  def _aggregateDailyHours(self):
    for collection in [self.worked, self.vacation, self.holidays, self.sick]:
      for date in collection:
        year, week, day = date.isocalendar()
        self.hoursPerDay[date] = self.hoursPerDay.get(date, 0) + \
              collection[date]

  def _aggregateWeeklyHours(self):
    for week in range(1, 54):
      self.hoursPerWeek[week] = 0.0

    for date in self.hoursPerDay:
      year, week, day = date.isocalendar()
      self.hoursPerWeek[week] += self.hoursPerDay[date]
      self.lastWeekEntered = max(self.lastWeekEntered, week)

  def _printReport(self,
         stream):
    balanceInHours = 0.0

    for week in range(1, self.lastWeekEntered + 1):
      weeklyBalanceInHours = self.hoursPerWeek[week] - self.contractHoursPerWeek
      stream.write("%2d: %+6g\n" % (week, weeklyBalanceInHours))
      balanceInHours += weeklyBalanceInHours

    stream.write("""\
balance      : %+g(h) / %+g(d)\n""" % (balanceInHours, balanceInHours / 8.0))

    hoursVacationTaken = 0.0

    for date in self.vacation:
      hoursVacationTaken += self.vacation[date]

    vacationBalanceInHours = self.vacationDaysPerYear * 8.0 - \
         hoursVacationTaken

    stream.write("""\
vacation left: %+g(h) / %+g(d)\n""" % (
         vacationBalanceInHours,
         vacationBalanceInHours / 8.0))

    hoursPerDay = []

    for date in self.hoursPerDay:
      hoursPerDay.append([date, self.hoursPerDay[date]])

    hoursPerDay.sort()

    for tuple_ in hoursPerDay[-15:]:
      stream.write("%s: %g\n" % (tuple_[0], tuple_[1]))

  def run(self):
    self.worked = self._parseHourInformation(self.workedStream)
    self.vacation = self._parseHourInformation(self.vacationStream)
    self.holidays = self._parseHourInformation(self.holidaysStream)
    self.sick = self._parseHourInformation(self.sickStream)

    self._aggregateDailyHours()
    self._aggregateWeeklyHours()

    self._printReport(sys.stdout)
    status = 0

    return status



if __name__ == "__main__":
  import optparse
  import sys

  usage = "usage: %prog [options] worked vacation holidays sick"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("", "--contract-hours",
           metavar="HOURS",
           action="store",
           type="float",
           dest="contractHours",
           default=40.0,
           help="contract HOURS per week (40.0)")
  parser.add_option("", "--vacation-days",
           metavar="DAYS",
           action="store",
           type="float",
           dest="vacationDays",
           default=0.0,
           help="amount of vacation DAYS (0.0)")

  (options, args) = parser.parse_args()

  if len(args) != 4:
    parser.print_help()
    sys.exit(1)

  # These files should not mention days that are not relevant for the job.
  worked   = args[0]    # Hours per days worked.
  vacation = args[1]    # Hours per vacation day.
  holidays = args[2]    # Hours per holiday.
  sick     = args[3]    # Hours per day sick.

  assert os.path.exists(worked) and os.path.isfile(worked), worked
  assert os.path.exists(vacation) and os.path.isfile(vacation), vacation
  assert os.path.exists(holidays) and os.path.isfile(holidays), holidays
  assert os.path.exists(sick) and os.path.isfile(sick), sick

  sys.exit(TimeTracker(
         file(worked, "r"),
         file(vacation, "r"),
         file(holidays, "r"),
         file(sick, "r"),
         options.contractHours,
         options.vacationDays).run())
