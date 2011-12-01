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
    stream = StringIO.StringIO()
    stream.write("# This is a comment\n")
    records = parser.parse(stream)
    self.assertEqual(len(records), 0)

  def test003(self):
    """Parse empty line"""
    parser = TrackTime.Parser()
    stream = StringIO.StringIO()
    stream.write("\n")
    records = parser.parse(stream)
    self.assertEqual(len(records), 0)

  def test004(self):
    """Parse line with only whitespace"""
    parser = TrackTime.Parser()
    stream = StringIO.StringIO()
    stream.write(" \n")
    stream.write("\t\n")
    records = parser.parse(stream)
    self.assertEqual(len(records), 0)

  def test011(self):
    """Parse <date>: <number of hours>"""
    # ParseError when same date more than once.
    # 20111201: 8
    pass

  def test021(self):
    """Parse <date>: <period>+"""
    # Error when same date more than once.
    pass

  def test022(self):
    """Parse mix of <date>: <number of hours>| <period>+"""
    pass

  def test031(self):
    """Parse <date>: <number of hours>: <project>"""
    # No error when same date more than once.
    pass

  def test041(self):
    """Parse <date>: <period>+: <project>"""
    # No error when same date more than once.
    pass

  def test051(self):
    """Parse Unicode characters"""
    pass
