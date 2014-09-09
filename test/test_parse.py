# -*- coding: utf-8 -*-
import datetime
import StringIO
import sys
import unittest
sys.path.append("../source")
import track_time


class TestParse(unittest.TestCase):

    def test_parse_project(self):
        project = track_time.parse_project("")
        self.assertEqual(len(project), 0)

        project = track_time.parse_project("/")
        self.assertEqual(len(project), 0)

        project = track_time.parse_project("//")
        self.assertEqual(len(project), 0)

        project = track_time.parse_project(" ")
        self.assertEqual(len(project), 0)

        project = track_time.parse_project("/ ")
        self.assertEqual(len(project), 0)

        project = track_time.parse_project(" /")
        self.assertEqual(len(project), 0)

        project = track_time.parse_project("blah")
        self.assertEqual(len(project), 1)
        self.assertEqual(project[0], "blah")

        project = track_time.parse_project("/blah")
        self.assertEqual(len(project), 1)
        self.assertEqual(project[0], "blah")

        project = track_time.parse_project("blah/")
        self.assertEqual(len(project), 1)
        self.assertEqual(project[0], "blah")

        project = track_time.parse_project("/blah/")
        self.assertEqual(len(project), 1)
        self.assertEqual(project[0], "blah")

        project = track_time.parse_project("blah/bloh")
        self.assertEqual(len(project), 2)
        self.assertEqual(project[0], "blah")
        self.assertEqual(project[1], "bloh")

        project = track_time.parse_project(" / blah / / bloh / ")
        self.assertEqual(len(project), 2)
        self.assertEqual(project[0], "blah")
        self.assertEqual(project[1], "bloh")

    def test001(self):
        """Parse empty file"""
        stream = StringIO.StringIO()
        records = track_time.parse(stream)
        self.assertEqual(len(records), 0)

    def test002(self):
        """Parse comment"""
        stream = StringIO.StringIO(
          "# This is a comment\n"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 0)

    def test003(self):
        """Parse empty line"""
        stream = StringIO.StringIO(
            "\n"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 0)

    def test004(self):
        """Parse line with only whitespace"""
        stream = StringIO.StringIO(
            " \n"
            "\t\n"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 0)

    def test010(self):
        """Parse <date>"""
        stream = StringIO.StringIO(
            "20111202\n"
            "20111205  # Comment..."
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8.0)
        self.assertEqual(len(record.project), 0)

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 8.0)
        self.assertEqual(len(record.project), 0)

    def test011(self):
        """Parse <date>: <number of hours>"""
        stream = StringIO.StringIO(
            "20111202: 8\n"
            "20111205: 4.5  # Comment..."
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8.0)
        self.assertEqual(len(record.project), 0)

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 4.5)
        self.assertEqual(len(record.project), 0)

        stream = StringIO.StringIO(
            "20111202: 8  # Comment...\n"
            "20111202: 4.5\n"
            "20111202: 3, 4"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 1)
        date = datetime.date(2011, 12, 2)

        self.assertEqual(len(records[date]), 3)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8.0)
        self.assertEqual(len(record.project), 0)

        record = records[date][1]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 4.5)
        self.assertEqual(len(record.project), 0)

        record = records[date][2]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 7.0)
        self.assertEqual(len(record.project), 0)

    def test021(self):
        """Parse <date>: <period>+"""
        stream = StringIO.StringIO(
            "20111202: 8:30-12:00, 12:30-17:00  # Comment...\n"
            "20111205: 10:00-12:15, 12:45-17:45"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8)
        self.assertEqual(len(record.project), 0)

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 7.25)
        self.assertEqual(len(record.project), 0)

    def test022(self):
        """Parse mix of <date>: <number of hours> | <period>+"""
        stream = StringIO.StringIO(
            "20111202: 4.5\n"
            "20111205: 10:00-12:15, 12:45-17:45  # Comment..."
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 4.5)
        self.assertEqual(len(record.project), 0)

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 7.25)
        self.assertEqual(len(record.project), 0)


        stream = StringIO.StringIO(
            "20111202: 4.5  # Comment...\n"
            "20111202: 10:00-12:15"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 1)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 2)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 4.5)
        self.assertEqual(len(record.project), 0)

        record = records[date][1]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 2.25)
        self.assertEqual(len(record.project), 0)


        stream = StringIO.StringIO(
            "20111202: 10:00-12:15, 4.5"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 1)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 6.75)
        self.assertEqual(len(record.project), 0)

    def test031(self):
        """Parse <date>: <number of hours>: <project>"""
        stream = StringIO.StringIO(
            "20121030: 3: project_x\n"
            "20121030: 5: project_y # Comment...\n"
            "20121031: 8: project_z"
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2012, 10, 30)
        self.assertEqual(len(records[date]), 2)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2012, 10, 30))
        self.assertEqual(record.nr_hours, 3.0)
        self.assertEqual(len(record.project), 1)
        self.assertEqual(record.project[0], "project_x")

        record = records[date][1]
        self.assertEqual(record.date, datetime.date(2012, 10, 30))
        self.assertEqual(record.nr_hours, 5.0)
        self.assertEqual(len(record.project), 1)
        self.assertEqual(record.project[0], "project_y")

        date = datetime.date(2012, 10, 31)
        self.assertEqual(len(records[date]), 1)

        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2012, 10, 31))
        self.assertEqual(record.nr_hours, 8.0)
        self.assertEqual(len(record.project), 1)
        self.assertEqual(record.project[0], "project_z")

    def test041(self):
        """Parse <date>: <period>+: <project>"""
        stream = StringIO.StringIO(
            "20111202: 8:30-12:00, 12:30-17:00: project_a\n"
            "20111205: 10:00-12:15, 12:45-17:45: project_b # Comment..."
        )
        records = track_time.parse(stream)
        self.assertEqual(len(records), 2)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8)
        self.assertEqual(len(record.project), 1)
        self.assertEqual(record.project[0], "project_a")

        date = datetime.date(2011, 12, 5)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 5))
        self.assertEqual(record.nr_hours, 7.25)
        self.assertEqual(len(record.project), 1)
        self.assertEqual(record.project[0], "project_b")

    def test051(self):
        """Parse Unicode characters"""
        stream = StringIO.StringIO(
            "20111202: 8:30-12:00, 12:30-17:00: prøject_ø # Cømment...\n"
        )

        records = track_time.parse(stream)
        self.assertEqual(len(records), 1)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(record.date, datetime.date(2011, 12, 2))
        self.assertEqual(record.nr_hours, 8)
        self.assertEqual(len(record.project), 1)
        self.assertEqual(record.project[0], "prøject_ø")

    def test061(self):
        """Parse sub-projects"""
        stream = StringIO.StringIO(
            "20111202: 8: a/b/c/d/e/f"
        )

        records = track_time.parse(stream)
        self.assertEqual(len(records), 1)

        date = datetime.date(2011, 12, 2)
        self.assertEqual(len(records[date]), 1)
        record = records[date][0]
        self.assertEqual(len(record.project), 6)
        self.assertEqual(record.project[0], "a")
        self.assertEqual(record.project[1], "b")
        self.assertEqual(record.project[2], "c")
        self.assertEqual(record.project[3], "d")
        self.assertEqual(record.project[4], "e")
        self.assertEqual(record.project[5], "f")

    def test101(self):
        """Parse error when input is wrongly formatted"""
        lines = [
            "20111202:",
            "20111202: project_a",
            "201x1202: 8",
            "20111202: 8:05-9x",
        ]

        for line in lines:
            with self.assertRaises(ValueError) as context_manager:
                stream = StringIO.StringIO(
                  line
                )
                records = track_time.parse(stream)
            exception = context_manager.exception
            self.assert_(str(exception).find("Parse error") != -1)
            # self.assertEqual(str(exception), "Parse error: {}".format(line))


if __name__ == "__main__":
    unittest.main()
