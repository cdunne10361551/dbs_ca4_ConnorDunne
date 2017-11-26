#Name: Connor Dunne
#Student Number: 10361551
#Import Log File Test
#This programme tests our log file import functions to see if our file is importing the way we expect

from ConnorDunne_10361551_CA4 import LogFileImport #import LogFileImport module from file
import unittest   #import unit test to run self assertion tests to ensure exact value is calculated
changes_file = 'changes_python.log'   #assign global variable for the reading log

class TestLogFileImport(unittest.TestCase):

    def setUp(self):
        self.logger = LogFileImport()   #assign LogFileImport() function to self.logger
	
	#Test log import 
    def test_import_for_correct_number_of_objects(self):
        #check correct legth of file
        fileimp = self.logger.read_file(changes_file)
        result = len(fileimp)
        self.assertEqual(5255, result)
        #check correct number of objects extracted
        fileorg = self.logger.get_commits(fileimp)
        result = len(fileorg)
        self.assertEqual(422, result)
        #check that dates are preprocessed before being cleaned (Not Equal)
        result = len(fileorg["date"][102])
        self.assertNotEqual(19, result)
        #check date has been processed correctly
        dateclean = self.logger.clean_dates(fileorg["date"])
        fileorg["date"] = dateclean
        result = len(fileorg["date"][76])
        self.assertEqual(19,result)
        #test file type is pandas DataFrame
        result = str(type(fileorg))
        self.assertEqual("<class 'pandas.core.frame.DataFrame'>",result)
if __name__ == '__main__':
    unittest.main()