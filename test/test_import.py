# -*- coding: utf-8 -*-
import inspect
import sys
import unittest
sys.path.append("../source")
import track_time


class TestImport(unittest.TestCase):

    def _testFunctionsInModule(self,
            module,
            functionNames):
        functionNamesInModule = [pair[0] for pair in inspect.getmembers(module,
            lambda member: inspect.isfunction(member))]
        for functionName in functionNames:
            self.assertTrue(functionName in functionNamesInModule, functionName)

    def _testClassesInModule(self,
            module,
            classNames):
        classNamesInModule = [pair[0] for pair in inspect.getmembers(module,
            lambda member: inspect.isclass(member))]
        for className in classNames:
            self.assertTrue(className in classNamesInModule, className)

    ### def testImportAll(self):
    ###   module = __import__("NetCDFTool.DataService", globals(), locals(),
    ###     ["*"], -1)
    ###   self.assertTrue(inspect.ismodule(module))

    ###   self.assertTrue("WcsDataset" in module.__dict__)
    ###   self.assertTrue("DataServiceConnection" in module.__dict__)
    ###   self.assertTrue("WcsConnection" in module.__dict__)
    ###   self.assertTrue("TdsConnection" in module.__dict__)

    ### def testImportTrackTime(self):
    ###     module = __import__("track_time")
    ###     module = sys.modules["track_time"]
    ###     self.assertTrue(inspect.ismodule(module))
    ###     self._testFunctionsInModule(module, [
    ###         "parse"
    ###     ])
    ###     self._testClassesInModule(module, [
    ###         "Aggregator",
    ###         "Record"
    ###     ])

    ### def testImportNetCDF_Analysis(self):
    ###   module = __import__("NetCDFTool.Analysis")
    ###   module = sys.modules["NetCDFTool.Analysis"]
    ###   self.assertTrue(inspect.ismodule(module))
    ###   self._testFunctionsInModule(module, [
    ###     "getVariableStatistics",
    ###     "temporalStatistics",
    ###   ])

    ### def testImportNetCDF_DataManagement(self):
    ###   module = __import__("NetCDFTool.DataManagement")
    ###   module = sys.modules["NetCDFTool.DataManagement"]
    ###   self.assertTrue(inspect.ismodule(module))
    ###   self._testFunctionsInModule(module, [
    ###     "appendByDimension",
    ###     "clip",
    ###     "extractByDimension",
    ###     "extractByVariable",
    ###   ])

    ### def testImportNetCDF_DataService(self):
    ###   module = __import__("NetCDFTool.DataService")
    ###   module = sys.modules["NetCDFTool.DataService"]
    ###   self.assertTrue(inspect.ismodule(module))
    ###   self._testClassesInModule(module, [
    ###     "WcsDataset",
    ###     "DataServiceConnection",
    ###     "WcsConnection",
    ###     "TdsConnection",
    ###   ])


if __name__ == "__main__":
    unittest.main()
