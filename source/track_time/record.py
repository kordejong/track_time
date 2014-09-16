# -*- coding: utf-8 -*-
"""
record
******
"""
import datetime


class Record(object):
    """
    Record keeps track of information on one line from an in input stream. An
    input stream contains the information of hours spent on work-related
    things.
    """

    def __init__(self,
            date,
            nr_hours,
            project=[]):
        """
        Create a record instance.
        """
        assert date is None or isinstance(date, datetime.date)
        assert isinstance(nr_hours, float)
        assert nr_hours <= 24.0
        self.date = date
        self.nr_hours = nr_hours
        self.project = project if len(project) > 0 else [""]

    # def __str__(self):
    #   return "{0}: {1}".format(self.date, self.nr_hours)

    @property
    def nr_days(self):
        return self.nr_hours / 8.0

    def project_string(self):
        return "/".join(self.project)

    def __iadd__(self,
            other):
        # r1 += r2
        self.date = None
        self.nr_hours += other.nr_hours
        return self

    def __repr__(self):
        return "Record(date={}, nr_hours={}, project={})".format(self.date,
            self.nr_hours, self.project_string())
