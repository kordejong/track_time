# -*- coding: utf-8 -*-
"""
Aggregator
**********
"""



class Aggregator(object):
  """
  Aggregator for aggregating records with information about hours spent working
  per day and project.
  """

  def __init__(self,
    records):
    """
    Create an Aggregator instance.
    """
    self.records = records

