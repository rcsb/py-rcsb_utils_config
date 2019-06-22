##
# File:    ConfigUtilTests.py
# Author:  J. Westbrook
# Date:    24-Aug-2018
# Version: 0.001
#
# Updates:
#  13-Sep-2018 jdw add YAML support and read/write methods.
#  10-Mar-2019 jdw add tests for .getEnvValue()
#
##
"""
Test cases for configuration utilities -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import time
import unittest
from collections import OrderedDict

from rcsb.utils.config.ConfigUtil import ConfigUtil

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigUtilTests(unittest.TestCase):
    def setUp(self):
        self.__verbose = True
        #
        self.__mockTopPath = os.path.abspath(os.path.dirname(__file__))
        self.__inpPathConfigIni = os.path.join(self.__mockTopPath, "setup-example.cfg")
        self.__inpPathConfigWithEnvIni = os.path.join(self.__mockTopPath, "setup-example-with-env.cfg")
        self.__inpPathConfigYaml = os.path.join(self.__mockTopPath, "setup-example.yml")
        self.__outPathConfigIni = os.path.join(self.__mockTopPath, "test-output", "out-setup-example.cfg")
        self.__outPathConfigWithEnvIni = os.path.join(self.__mockTopPath, "test-output", "out-setup-example-with-env.cfg")
        self.__outPathConfigYaml = os.path.join(self.__mockTopPath, "test-output", "out-setup-example.yml")
        self.__outPathConfigYamlExport = os.path.join(self.__mockTopPath, "test-output", "out-export-example.yml")
        #
        self.__cfgOb = ConfigUtil(configPath=self.__inpPathConfigIni, mockTopPath=self.__mockTopPath)
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def testReadIniConfigWithEnv(self):
        try:
            os.environ["TEST_MOCKPATH_ENV"] = self.__mockTopPath
            cfgOb = ConfigUtil(configPath=self.__inpPathConfigWithEnvIni, mockTopPath=self.__mockTopPath, importEnvironment=True)
            testEnv = cfgOb.get("test_mockpath_env")
            self.assertEqual(testEnv, self.__mockTopPath)
            logger.debug("Environmental variable test_mock_path is %r", testEnv)
            #  Verify environment keys all lowercased -
            testEnv = cfgOb.get("TEST_MOCKPATH_ENV")
            self.assertEqual(testEnv, None)
            logger.debug("Environmental variable TEST_MOCK_PATH is %r", testEnv)
            #
            testEnv = cfgOb.get("TOP_PROJECT_PATH")
            self.assertEqual(testEnv, self.__mockTopPath)
            logger.debug("Derived path is %r", testEnv)
            #
            sName = "Section1"
            testEnv = cfgOb.get("PROJ_DIR_PATH", sectionName=sName)
            self.assertEqual(testEnv, os.path.join(self.__mockTopPath, "da_top"))

            testEnv = cfgOb.get("PROJ_ARCHIVE_PATH", sectionName=sName)
            self.assertEqual(testEnv, os.path.join(self.__mockTopPath, "da_top", "archive"))

            testEnv = cfgOb.get("proj_deposit_path", sectionName=sName)
            self.assertEqual(testEnv, os.path.join(self.__mockTopPath, "da_top", "deposit"))
            #
            ok = cfgOb.writeConfig(self.__outPathConfigWithEnvIni, configFormat="ini")
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()
        return {}

    def testReadIniConfig(self):
        try:
            sName = "DEFAULT"
            pathBird = self.__cfgOb.getPath("BIRD_REPO_PATH", sectionName=sName)
            pathPdbx = self.__cfgOb.getPath("PDBX_REPO_PATH", sectionName=sName)
            #
            self.assertEqual(pathBird, os.path.join(self.__mockTopPath, "MOCK_BIRD_REPO"))
            self.assertEqual(pathPdbx, os.path.join(self.__mockTopPath, "MOCK_PDBX_SANDBOX"))

            pathBird = self.__cfgOb.get("BIRD_REPO_PATH", sectionName=sName)
            pathPdbx = self.__cfgOb.get("PDBX_REPO_PATH", sectionName=sName)

            self.assertEqual(pathBird, "MOCK_BIRD_REPO")
            self.assertEqual(pathPdbx, "MOCK_PDBX_SANDBOX")
            sName = "Section1"
            #
            helperMethod = self.__cfgOb.getHelper("DICT_METHOD_HELPER_MODULE", sectionName=sName)

            tv = helperMethod.echo("test_value")
            self.assertEqual(tv, "test_value")
            #
            tEnv = "TEST_ENV_VAR"
            tVal = "TEST_ENV_VAR_VALUE"
            os.environ[tEnv] = tVal
            eVal = self.__cfgOb.getEnvValue("ENV_OPTION_A", sectionName=sName)
            self.assertEqual(tVal, eVal)
            #
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()
        return {}

    def testWriteFromIniConfig(self):
        try:
            ok = self.__cfgOb.writeConfig(self.__outPathConfigIni, configFormat="ini")
            ok = self.__cfgOb.writeConfig(self.__outPathConfigYaml, configFormat="yaml")
            self.assertTrue(ok)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()
        return {}

    def testReadYamlConfig(self):
        try:
            cfgOb = ConfigUtil(configPath=self.__inpPathConfigYaml, configFormat="yaml", mockTopPath=self.__mockTopPath)
            sName = "DEFAULT"
            pathBird = cfgOb.getPath("BIRD_REPO_PATH", sectionName=sName)
            pathPdbx = cfgOb.getPath("PDBX_REPO_PATH", sectionName=sName)
            #
            self.assertEqual(pathBird, os.path.join(self.__mockTopPath, "MOCK_BIRD_REPO"))
            self.assertEqual(pathPdbx, os.path.join(self.__mockTopPath, "MOCK_PDBX_SANDBOX"))

            pathBird = cfgOb.get("BIRD_REPO_PATH", sectionName=sName)
            pathPdbx = cfgOb.get("PDBX_REPO_PATH", sectionName=sName)

            self.assertEqual(pathBird, "MOCK_BIRD_REPO")
            self.assertEqual(pathPdbx, "MOCK_PDBX_SANDBOX")
            sName = "Section1"
            #
            helperMethod = cfgOb.getHelper("DICT_METHOD_HELPER_MODULE", sectionName=sName)

            tv = helperMethod.echo("test_value")
            self.assertEqual(tv, "test_value")
            #
            tEnv = "TEST_ENV_VAR"
            tVal = "TEST_ENV_VAR_VALUE"
            os.environ[tEnv] = tVal
            eVal = cfgOb.getEnvValue("ENV_OPTION_A", sectionName=sName)
            self.assertEqual(tVal, eVal)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()
        return {}

    def testWriteFromYamlConfig(self):
        try:
            cfgOb = ConfigUtil(configPath=self.__inpPathConfigYaml, configFormat="yaml", mockTopPath=self.__mockTopPath)
            ok = cfgOb.writeConfig(self.__outPathConfigIni, configFormat="ini")
            self.assertTrue(ok)
            ok = cfgOb.writeConfig(self.__outPathConfigYaml, configFormat="yaml")
            self.assertTrue(ok)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()
        return {}

    def testRoundTripYaml(self):
        try:
            cfgOb = ConfigUtil(configPath=self.__inpPathConfigYaml, configFormat="yaml", mockTopPath=self.__mockTopPath)
            ok = cfgOb.writeConfig(self.__outPathConfigIni, configFormat="ini")
            self.assertTrue(ok)
            ok = cfgOb.writeConfig(self.__outPathConfigYaml, configFormat="yaml")
            self.assertTrue(ok)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()
        return {}

    def __createDataSet(self):
        dD = {"Name": "THE_NAME", "Location": "/a/b/c/loc.dat", "Date": "2017-09-18", "Counts": [1, 2, 3], "Measured": 1.1234}
        rD = OrderedDict()
        for section in ["Section1", "Section2", "Section3"]:
            rD[section] = {}
            for subSection in ["SubA", "SubB", "SubC"]:
                rD[section][subSection] = dD
                # for ii in range(5):
                #    rD[section][subSection].append(copy.deepcopy(d))
        return rD

    def testExportToYaml(self):
        cfgOb = ConfigUtil(configFormat="yaml", mockTopPath=self.__mockTopPath)
        #
        cD = self.__createDataSet()
        cfgOb.importConfig(cD)
        #
        ok = cfgOb.writeConfig(self.__outPathConfigYamlExport, configFormat="yaml")
        self.assertTrue(ok)
        cfgOb = ConfigUtil(configPath=self.__outPathConfigYamlExport, configFormat="yaml", mockTopPath=self.__mockTopPath)
        rD = cfgOb.exportConfig()
        self.assertGreaterEqual(len(rD), 1)
        v = cfgOb.get("SubA.Name", sectionName="Section1")
        self.assertEqual(v, "THE_NAME")
        v = cfgOb.get("SubA.Counts", sectionName="Section3")
        self.assertEqual(len(v), 3)


def suiteConfigAccess():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigUtilTests("testReadIniConfig"))
    suiteSelect.addTest(ConfigUtilTests("testReadIniConfigWithEnv"))
    suiteSelect.addTest(ConfigUtilTests("testWriteFromIniConfig"))
    suiteSelect.addTest(ConfigUtilTests("testReadYamlConfig"))
    suiteSelect.addTest(ConfigUtilTests("testWriteFromYamlConfig"))
    suiteSelect.addTest(ConfigUtilTests("testExportToYaml"))
    return suiteSelect


if __name__ == "__main__":
    # Run all tests --
    # unittest.main()
    #
    mySuite = suiteConfigAccess()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
