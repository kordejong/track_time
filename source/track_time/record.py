# -*- coding: utf-8 -*-
"""
record
******
"""
import datetime


class Record(object):
    """
    Record keeps track of information on one line from an in input stream. An
    input stream contains the information of hours spent working per day per
    project.
    """

    def __init__(self,
            date,
            nr_hours,
            project=None):
        """
        Create a record instance.
        """
        assert(isinstance(date, datetime.date))
        assert(isinstance(nr_hours, float))
        assert(nr_hours <= 24.0)
        self.date = date
        self.nr_hours = nr_hours
        self.project=project

    # def __str__(self):
    #   return "{0}: {1}".format(self.date, self.nr_hours)

    def __repr__(self):
        return "Record(date={}, nr_hours={}, project={})".format(self.date,
            self.nr_hours, self.project)
