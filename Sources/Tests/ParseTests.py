# -*- coding: utf-8 -*-
import datetime
import StringIO
import unittest
import TrackTime



class ParseTests(unittest.TestCase):

  def test001(self):
    """Parse empty file"""
    parser = TrackTime.Parser()
    stream = StringIO.StringIO()
    records = parser.parse(stream)
    self.assertEqual(len(records), 0)

  def test002(self):
    """Parse comment"""
    parser = TrackTime.Parser()
    stream = StringIO.StringIO(
      "# This is a comment\n"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 0)

  def test003(self):
    """Parse empty line"""
    parser = TrackTime.Parser()
    stream = StringIO.StringIO(
      "\n"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 0)

  def test004(self):
    """Parse line with only whitespace"""
    parser = TrackTime.Parser()
    stream = StringIO.StringIO(
      " \n"
      "\t\n"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 0)

  def test011(self):
    """Parse <date>: <number of hours>"""
    parser = TrackTime.Parser()

    stream = StringIO.StringIO(
      "20111202: 8\n"
      "20111205: 4.5"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 2)

    date = datetime.date(2011, 12, 2)
    self.assertEqual(len(records[date]), 1)
    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 2))
    self.assertEqual(record.nrHours, 8.0)

    date = datetime.date(2011, 12, 5)
    self.assertEqual(len(records[date]), 1)
    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 5))
    self.assertEqual(record.nrHours, 4.5)

    stream = StringIO.StringIO(
      "20111202: 8\n"
      "20111202: 4.5"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 1)
    date = datetime.date(2011, 12, 2)

    self.assertEqual(len(records[date]), 2)
    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 2))
    self.assertEqual(record.nrHours, 8.0)
    record = records[date][1]
    self.assertEqual(record.date, datetime.date(2011, 12, 2))
    self.assertEqual(record.nrHours, 4.5)

  def test021(self):
    """Parse <date>: <period>+"""
    parser = TrackTime.Parser()

    stream = StringIO.StringIO(
      "20111202: 8:30-12:00, 12:30-17:00\n"
      "20111205: 10:00-12:15, 12:45-17:45"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 2)

    date = datetime.date(2011, 12, 2)
    self.assertEqual(len(records[date]), 1)
    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 2))
    self.assertEqual(record.nrHours, 8)

    date = datetime.date(2011, 12, 5)
    self.assertEqual(len(records[date]), 1)
    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 5))
    self.assertEqual(record.nrHours, 7.25)

  def test022(self):
    """Parse mix of <date>: <number of hours>| <period>+"""
    parser = TrackTime.Parser()

    stream = StringIO.StringIO(
      "20111202: 4.5\n"
      "20111205: 10:00-12:15, 12:45-17:45"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 2)

    date = datetime.date(2011, 12, 2)
    self.assertEqual(len(records[date]), 1)
    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 2))
    self.assertEqual(record.nrHours, 4.5)

    date = datetime.date(2011, 12, 5)
    self.assertEqual(len(records[date]), 1)
    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 5))
    self.assertEqual(record.nrHours, 7.25)

    stream = StringIO.StringIO(
      "20111202: 4.5\n"
      "20111202: 10:00-12:15"
    )
    records = parser.parse(stream)
    self.assertEqual(len(records), 1)

    date = datetime.date(2011, 12, 2)
    self.assertEqual(len(records[date]), 2)

    record = records[date][0]
    self.assertEqual(record.date, datetime.date(2011, 12, 2))
    self.assertEqual(record.nrHours, 4.5)

    record = records[date][1]
    self.assertEqual(record.date, datetime.date(2011, 12, 2))
    self.assertEqual(record.nrHours, 2.25)

  def test031(self):
    """Parse <date>: <number of hours>: <project>"""
    pass

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

