# -*- coding: utf-8 -*-
"""
Aggregator
**********
"""
import datetime


class Aggregator(object):
    """
    Aggregator for aggregating records with information about how many hours
    are spent on what (work, sick, holiday, vacation) and on what project.
    """

    def __init__(self,
            contract_hours_per_week,
            vacation_days_per_year,
            hours_worked,
            hours_sick,
            hours_vacation,
            hours_holiday):
        """
        Create an Aggregator instance.
        """
        self.contract_hours_per_week = contract_hours_per_week
        self.vacation_days_per_year = vacation_days_per_year
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
                        self.hours_per_day.get(date, 0.0) + record.nr_hours

        days = self.hours_per_day.keys()
        days.sort()

        year = datetime.timedelta(days=365)
        if (days[-1] - days[0]) > year:
            raise ValueError(
                "No support for records from more than one year, yet")

        # Aggregate per week.
        self.hours_per_week = {}
        for date in self.hours_per_day:
            year, week, day = date.isocalendar()
            self.hours_per_week[week] = self.hours_per_week.get(week, 0.0) + \
                self.hours_per_day[date]

    def print_report(self,
            stream):
        balance_in_hours = 0.0

        for week in range(min(self.hours_per_week.keys()),
                max(self.hours_per_week.keys()) + 1):
            weekly_balance_in_hours = self.hours_per_week[week] - \
                self.contract_hours_per_week
            stream.write("%2d: %+6g\n" % (week, weekly_balance_in_hours))
            balance_in_hours += weekly_balance_in_hours

        stream.write("balance      : %+g(h) / %+g(d)\n" % (balance_in_hours,
            balance_in_hours / 8.0))

        hours_vacation_taken = 0.0
        for date in self.hours_vacation:
            for record in self.hours_vacation[date]:
                hours_vacation_taken += record.nr_hours

        vacation_balance_in_hours = self.vacation_days_per_year * 8.0 - \
             hours_vacation_taken

        stream.write("vacation left: %+g(h) / %+g(d)\n" % (
            vacation_balance_in_hours,
            vacation_balance_in_hours / 8.0))

        hours_per_day = []

        for date in self.hours_per_day:
            hours_per_day.append([date, self.hours_per_day[date]])

        hours_per_day.sort()

        for tuple_ in hours_per_day[-15:]:
            stream.write("%s: %g\n" % (tuple_[0], tuple_[1]))
