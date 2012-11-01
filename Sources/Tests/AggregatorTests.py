# -*- coding: utf-8 -*-
import sys
import unittest
sys.path.append("..")
import TrackTime


class AggregatorTests(unittest.TestCase):

    def test001(self):
        """Test typical behavior"""
        hours_worked = TrackTime.parse(file("Work-001.txt"))
        hours_sick = TrackTime.parse(file("Sick-001.txt"))
        hours_vacation = TrackTime.parse(file("Vacation-001.txt"))
        hours_holiday = TrackTime.parse(file("Holiday-001.txt"))

        aggregator = TrackTime.Aggregator(hours_worked, hours_sick,
            hours_vacation, hours_holiday)

        # print aggregator.hours_per_day
        # print aggregator.hours_per_week
        # print max(aggregator.hours_per_week.keys())
        aggregator.print_report(sys.stdout)


if __name__ == "__main__":
    unittest.main()
