# -*- coding: utf-8 -*-
"""
Record
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
    nrHours):
    """
    Create a record instance.
    """
    assert(isinstance(date, datetime.date))
    assert(isinstance(nrHours, float))
    assert(nrHours <= 24.0)
    self.date = date
    self.nrHours = nrHours

  # def __str__(self):
  #   return "{0}: {1}".format(self.date, self.nrHours)

  def __repr__(self):
    return "Record(date={0}, nrHours={1})".format(self.date, self.nrHours)

