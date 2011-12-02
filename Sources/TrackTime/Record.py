# -*- coding: utf-8 -*-
"""
Record
******
"""



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
    # date/time, period/nrHours, project
    self.date = date
    self.nrHours = nrHours

