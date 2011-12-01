import os
import sys
import unittest



sys.path = [
  os.path.join(os.environ["TRACKTIME"], "Sources")
] + sys.path



if __name__ == "__main__":
  unittest.TextTestRunner(verbosity=2).run(
    unittest.TestLoader().loadTestsFromNames([
      "ImportTests.ImportTests",
      "ParseTests.ParseTests",
    ]
  )
)
