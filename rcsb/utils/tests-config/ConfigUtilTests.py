##
# File:    ConfigUtilTests.py
# Author:  J. Westbrook
# Date:    24-Aug-2018
# Version: 0.001
#
# Updates:
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

from rcsb.utils.config.ConfigUtil import ConfigUtil

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigUtilTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        #
        self.__mockTopPath = os.path.abspath(os.path.dirname(__file__))
        self.__pathConfig = os.path.join(self.__mockTopPath, 'setup-example.cfg')
        #
        self.__cfgOb = ConfigUtil(configPath=self.__pathConfig, mockTopPath=self.__mockTopPath)
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def testConfigAccess(self):
        try:
            sName = 'DEFAULT'
            pathBird = self.__cfgOb.getPath('BIRD_REPO_PATH', sectionName=sName)
            pathPdbx = self.__cfgOb.getPath('PDBX_REPO_PATH', sectionName=sName)
            #
            self.assertEqual(pathBird, os.path.join(self.__mockTopPath, 'MOCK_BIRD_REPO'))
            self.assertEqual(pathPdbx, os.path.join(self.__mockTopPath, 'MOCK_PDBX_SANDBOX'))

            pathBird = self.__cfgOb.get('BIRD_REPO_PATH', sectionName=sName)
            pathPdbx = self.__cfgOb.get('PDBX_REPO_PATH', sectionName=sName)

            self.assertEqual(pathBird, 'MOCK_BIRD_REPO')
            self.assertEqual(pathPdbx, 'MOCK_PDBX_SANDBOX')
            sName = 'section1'
            #
            helperMethod = self.__cfgOb.getHelper('DICT_METHOD_HELPER_MODULE', sectionName=sName)

            tv = helperMethod.echo('test_value')
            self.assertEqual(tv, 'test_value')

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()
        return {}


def suiteConfigAccess():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigUtilTests("testConfigAccess"))
    return suiteSelect


if __name__ == '__main__':
    # Run all tests --
    # unittest.main()
    #
    mySuite = suiteConfigAccess()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
