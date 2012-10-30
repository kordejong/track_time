# -*- coding: utf-8 -*-
import sys
import unittest
sys.path.append("..")
import TrackTime


class AggregatorTests(unittest.TestCase):

    def test001(self):
        """Test typical behavior"""
        hours_worked = TrackTime.parse(file("WorkedHours-001.txt"))
        hours_sick = {}
        hours_vacation = {}
        hours_holiday = {}

        aggregator = TrackTime.Aggregator(hours_worked, hours_sick,
            hours_vacation, hours_holiday)


if __name__ == "__main__":
    unittest.main()
