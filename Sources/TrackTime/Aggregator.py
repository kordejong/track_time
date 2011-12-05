# -*- coding: utf-8 -*-
"""
Aggregator
**********
"""
import datetime



class Aggregator(object):
  """
  Aggregator for aggregating records with information about hours spent working
  per day and project.
  """

  def __init__(self,
    workedHours,
    sickHours,
    vacationHours,
    holidayHours):
    """
    Create an Aggregator instance.
    """
    self.workedHours = workedHours
    self.sickHours = sickHours
    self.vacationHours = vacationHours
    self.holidayHours = holidayHours

    # Aggregate per day.
    self.hoursPerDay = {}
    for collection in [self.workedHours, self.sickHours, self.vacationHours,
      self.holidayHours]:
      for date in collection:
        year, week, day = date.isocalendar()
        recordsPerDay = collection[date]

        for record in recordsPerDay:
          self.hoursPerDay[date] = self.hoursPerDay.get(date, 0) + \
            record.nrHours

    days = self.hoursPerDay.keys()
    days.sort()

    year = datetime.timedelta(days=365)
    if (days[-1] - days[0]) > year:
      raise ValueError("No support for records from more than one year, yet")

    # Aggregate per week.
    self.hoursPerWeek = {}
    for week in range(1, 54):
      self.hoursPerWeek[week] = 0.0

    for date in self.hoursPerDay:
      year, week, day = date.isocalendar()
      self.hoursPerWeek[week] += self.hoursPerDay[date]
      # self.lastWeekEntered = max(self.lastWeekEntered, week)


