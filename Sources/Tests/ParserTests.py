# -*- coding: utf-8 -*-
import datetime
import StringIO
import sys
import unittest
sys.path.append("..")
import TrackTime


class ParserTests(unittest.TestCase):

    def test001(self):
        """Parse empty file"""
        stream = StringIO.StringIO()
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 0)

    def test002(self):
        """Parse comment"""
        stream = StringIO.StringIO(
          "# This is a comment\n"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 0)

    def test003(self):
        """Parse empty line"""
        stream = StringIO.StringIO(
            "\n"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 0)

    def test004(self):
        """Parse line with only whitespace"""
        stream = StringIO.StringIO(
            " \n"
            "\t\n"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 0)

    def test011(self):
        """Parse <date>: <number of hours>"""
        stream = StringIO.StringIO(
            "20111202: 8\n"
            "20111205: 4.5"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8.0)
        self.assert_(record.project is None)

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 4.5)
        self.assert_(record.project is None)

        stream = StringIO.StringIO(
            "20111202: 8\n"
            "20111202: 4.5"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 1)
        date = datetime.date(2011, 12, 2)

        self.assertEqual(len(records[date]), 2)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8.0)
        self.assert_(record.project is None)

        record = records[date][1]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 4.5)
        self.assert_(record.project is None)

    def test021(self):
        """Parse <date>: <period>+"""
        stream = StringIO.StringIO(
            "20111202: 8:30-12:00, 12:30-17:00\n"
            "20111205: 10:00-12:15, 12:45-17:45"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8)
        self.assert_(record.project is None)

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 7.25)
        self.assert_(record.project is None)

    def test022(self):
        """Parse mix of <date>: <number of hours>| <period>+"""
        stream = StringIO.StringIO(
            "20111202: 4.5\n"
            "20111205: 10:00-12:15, 12:45-17:45"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 4.5)
        self.assert_(record.project is None)

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 7.25)
        self.assert_(record.project is None)

        stream = StringIO.StringIO(
            "20111202: 4.5\n"
            "20111202: 10:00-12:15"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 1)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 2)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 4.5)
        self.assert_(record.project is None)

        record = records[date][1]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 2.25)
        self.assert_(record.project is None)

    def test031(self):
        """Parse <date>: <number of hours>: <project>"""
        stream = StringIO.StringIO(
            "20121030: 3: project_x\n"
            "20121030: 5: project_y\n"
            "20121031: 8: project_z"
        )
        records = TrackTime.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2012, 10, 30)
        self.assertEqual(len(records[date]), 2)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2012, 10, 30))
        self.assertEqual(record.nr_hours, 3.0)
        self.assertEqual(record.project, "project_x")

        record = records[date][1]
        self.assertEqual(record.date, datetime.date(2012, 10, 30))
        self.assertEqual(record.nr_hours, 5.0)
        self.assertEqual(record.project, "project_y")

        date = datetime.date(2012, 10, 31)
        self.assertEqual(len(records[date]), 1)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2012, 10, 31))
        self.assertEqual(record.nr_hours, 8.0)
        self.assertEqual(record.project, "project_z")

    def test041(self):
        """Parse <date>: <period>+: <project>"""
        pass

    def test051(self):
        """Parse Unicode characters"""
        pass

    def test101(self):
        """Parse error when input is wrongly formatted"""
        # with self.assertRaises(ValueError) as contextManager:
        #   StringIO.StringIO(
        #     "20111202: 8\n"
        #     "20111202: 4"
        #   )
        # exception = contextManager.exception
        # self.assertEqual(str(exception), "Balbal")
        pass


if __name__ == "__main__":
    unittest.main()
