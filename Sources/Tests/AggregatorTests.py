# -*- coding: utf-8 -*-
import unittest
import TrackTime



class AggregatorTests(unittest.TestCase):

  def test001(self):
    """Test typical behavior"""
    parser = TrackTime.Parser()
    workedHours = parser.parse(file("WorkedHours-001.txt"))
    sickHours = {}
    vacationHours = {}
    holidayHours = {}

    aggregator = TrackTime.Aggregator(workedHours, sickHours, vacationHours,
      holidayHours)


