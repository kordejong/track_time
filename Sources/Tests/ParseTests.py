import unittest



class ParseTests(unittest.TestCase):

  def test001(self):
    """Parse empty file"""
    pass

  def test002(self):
    """Parse comment"""
    pass

  def test011(self):
    """Parse <date>: <number of hours>"""
    # Error when same date more than once.
    pass

  def test021(self):
    """Parse <date>: <period>+"""
    # Error when same date more than once.
    pass

  def test031(self):
    """Parse <date>: <number of hours>: <project>"""
    # No error when same date more than once.
    pass

  def test041(self):
    """Parse <date>: <period>+: <project>"""
    # No error when same date more than once.
    pass


