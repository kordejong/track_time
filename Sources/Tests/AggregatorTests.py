# -*- coding: utf-8 -*-
import datetime
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

        aggregator = TrackTime.Aggregator(16, 8, hours_worked, hours_sick,
            hours_vacation, hours_holiday)

        hours_per_day = aggregator.hours_per_day
        self.assertEqual(len(hours_per_day), 4)
        self.assertEqual(hours_per_day[datetime.date(2013, 1, 1)], 8.0)
        self.assertEqual(hours_per_day[datetime.date(2013, 1, 2)], 8.0)
        self.assertEqual(hours_per_day[datetime.date(2013, 1, 3)], 8.0)
        self.assertEqual(hours_per_day[datetime.date(2013, 1, 4)], 8.0)

        hours_per_week = aggregator.hours_per_week
        self.assertEqual(len(hours_per_week), 1)
        self.assertEqual(hours_per_week[1], 32.0)

        # aggregator.print_report(sys.stdout)


if __name__ == "__main__":
    unittest.main()
