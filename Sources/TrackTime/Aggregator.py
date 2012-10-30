# -*- coding: utf-8 -*-
"""
Aggregator
**********
"""
import datetime


class Aggregator(object):
    """
    Aggregator for aggregating records with information about hours spent
    working per day and project.
    """

    def __init__(self,
            hours_worked,
            hours_sick,
            hours_vacation,
            hours_holiday):
        """
        Create an Aggregator instance.
        """
        self.hours_worked = hours_worked
        self.hours_sick = hours_sick
        self.hours_vacation = hours_vacation
        self.hours_holiday = hours_holiday

        # Aggregate per day.
        self.hours_per_day = {}
        for collection in [self.hours_worked, self.hours_sick,
                self.hours_vacation, self.hours_holiday]:
            for date in collection:
                year, week, day = date.isocalendar()
                records_per_day = collection[date]

                for record in records_per_day:
                    self.hours_per_day[date] = \
                        self.hours_per_day.get(date, 0) + record.nr_hours

        days = self.hours_per_day.keys()
        days.sort()

        year = datetime.timedelta(days=365)
        if (days[-1] - days[0]) > year:
            raise ValueError(
                "No support for records from more than one year, yet")

        # Aggregate per week.
        self.hours_per_week = {}
        for week in range(1, 54):
            self.hours_per_week[week] = 0.0

        for date in self.hours_per_day:
            year, week, day = date.isocalendar()
            self.hours_per_week[week] += self.hours_per_day[date]
            # self.last_week_entered = max(self.last_week_entered, week)
