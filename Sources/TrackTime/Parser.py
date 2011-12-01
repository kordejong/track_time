# -*- coding: utf-8 -*-
"""
Parser
******
"""
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
    return []

