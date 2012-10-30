# -*- coding: utf-8 -*-
import unittest


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromNames([
            "ImportTests.ImportTests",
            "ParserTests.ParserTests",
            "AggregatorTests.AggregatorTests",
        ]
    )
)
