import unittest
from RuleBasedTextParser import RuleBasedTextParser

class TestRuleBasedTextParser(unittest.TestCase):

    def setUp(self):
        print("\n\n[INFO] : Setting up RuleBasedTextParser Module.\n")
        self.rule = RuleBasedTextParser(None,'&','standard_definition.json','error_codes.json')
        # print(self.rule.sentence_dict)

    def tearDown(self):
        print("[INFO] : Nothing Done in tearDown function to Tore Down Environment.\n")

    def test_rule_based_parser_l1(self):
        print("[INFO] : Checking L1 Test Cases.\n")
        self.maxDiff = None
        
        # L1 test cases

        self.rule.sentence_dict = [['L1','1','ABC','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        # L1 test cases for missing or additional sub_sections

        self.rule.sentence_dict = [['L1']]
        self.assertEqual(self.rule.run_parser(),"L11 field under section L1 is missing.L12 field under section L1 is missing.L13 field under section L1 is missing.")

        self.rule.sentence_dict = [['L1','1']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under section L1 is missing.L13 field under section L1 is missing.")

        self.rule.sentence_dict = [['L1','1','ABC']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under section L1 is missing.")

        self.rule.sentence_dict = [['L1','1','ABC','AB','A']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.L14 field under section L1 is missing in standard definition file.")

        # L11 test cases

        self.rule.sentence_dict = [['L1','12','ABC','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under section L1 fails the max length (expected: 1) validation, however it passes the data type (digits) validation.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','A','ABC','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under section L1 fails the data type (expected: digits) validation, however it passes the max length (1) validation.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','AB','ABC','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under section L1 fails all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','','ABC','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under section L1 fails all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.")
        
        # L12 test cases

        self.rule.sentence_dict = [['L1','1','AB2','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','123','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under section L1 fails the data type (expected: word_characters) validation, however it passes the max length (3) validation.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','ABCD','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under section L1 fails the max length (expected: 3) validation, however it passes the data type (word_characters) validation.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','AB','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under section L1 fails the max length (expected: 3) validation, however it passes the data type (word_characters) validation.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under section L1 fails the max length (expected: 3) validation, however it passes the data type (word_characters) validation.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','1234','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under section L1 fails all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','12','AB']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under section L1 fails all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        # L13 test cases

        self.rule.sentence_dict = [['L1','1','ABC','A2']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','ABC','12']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under section L1 fails the data type (expected: word_characters) validation, however it passes the max length (2) validation.")

        self.rule.sentence_dict = [['L1','1','ABC','ABC']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under section L1 fails the max length (expected: 2) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L1','1','ABC','A']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under section L1 fails the max length (expected: 2) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L1','1','ABC','']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under section L1 fails the max length (expected: 2) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L1','1','ABC','123']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under section L1 fails all the validation criteria.")

        self.rule.sentence_dict = [['L1','1','ABC','1']]
        self.assertEqual(self.rule.run_parser(),"L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under section L1 fails all the validation criteria.")
        print("[INFO] : L1 Test Casses Passed.\n")

    def test_rule_based_parser_l2(self):
        print("[INFO] : Checking L2 Test Cases.\n")
        self.maxDiff = None

        # L2 test cases
        
        self.rule.sentence_dict = [['L2','A','1','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        # L2 test cases for missing or additional sub_sections
        
        self.rule.sentence_dict = [['L2']]
        self.assertEqual(self.rule.run_parser(),"L21 field under section L2 is missing.L22 field under section L2 is missing.L23 field under section L2 is missing.")

        self.rule.sentence_dict = [['L2','A']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under section L2 is missing.L23 field under section L2 is missing.")

        self.rule.sentence_dict = [['L2','A','1']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under section L2 is missing.")

        self.rule.sentence_dict = [['L2','A','1','AB','A']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under segment L2 passes all the validation criteria.L24 field under section L2 is missing in standard definition file.")

        # L21 test cases

        self.rule.sentence_dict = [['L2','AB','1','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under section L2 fails the max length (expected: 1) validation, however it passes the data type (word_characters) validation.L22 field under segment L2 passes all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','','1','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under section L2 fails the max length (expected: 1) validation, however it passes the data type (word_characters) validation.L22 field under segment L2 passes all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','1','1','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under section L2 fails the data type (expected: word_characters) validation, however it passes the max length (1) validation.L22 field under segment L2 passes all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','12','1','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under section L2 fails all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        # L22 test cases

        self.rule.sentence_dict = [['L2','A','A','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under section L2 fails the data type (expected: digits) validation, however it passes the max length (1) validation.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','A','12','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under section L2 fails the max length (expected: 1) validation, however it passes the data type (digits) validation.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','A','AB','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under section L2 fails all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','A','','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under section L2 fails all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','A','A2','AB']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under section L2 fails all the validation criteria.L23 field under segment L2 passes all the validation criteria.")


        # L23 test cases

        self.rule.sentence_dict = [['L2','A','1','A2']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under segment L2 passes all the validation criteria.")

        self.rule.sentence_dict = [['L2','A','1','12']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under section L2 fails the data type (expected: word_characters) validation, however it passes the max length (2) validation.")

        self.rule.sentence_dict = [['L2','A','1','ABC']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under section L2 fails the max length (expected: 2) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L2','A','1','A']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under section L2 fails the max length (expected: 2) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L2','A','1','']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under section L2 fails the max length (expected: 2) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L2','A','1','123']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under section L2 fails all the validation criteria.")

        self.rule.sentence_dict = [['L2','A','1','1']]
        self.assertEqual(self.rule.run_parser(),"L21 field under segment L2 passes all the validation criteria.L22 field under segment L2 passes all the validation criteria.L23 field under section L2 fails all the validation criteria.")

        print("[INFO] : L2 Test Casses Passed.\n")
    
    def test_rule_based_parser_l3(self):
        print("[INFO] : Checking L3 Test Cases.\n")
        self.maxDiff = None
    
        # L3 test cases
        
        self.rule.sentence_dict = [['L3','A']]
        self.assertEqual(self.rule.run_parser(),"L31 field under segment L3 passes all the validation criteria.")

        # L3 test cases for missing or additional sub_sections

        self.rule.sentence_dict = [['L3']]
        self.assertEqual(self.rule.run_parser(),"L31 field under section L3 is missing.")

        self.rule.sentence_dict = [['L3','A','AB']]
        self.assertEqual(self.rule.run_parser(),"L31 field under segment L3 passes all the validation criteria.L32 field under section L3 is missing in standard definition file.")

        # L31 test cases

        self.rule.sentence_dict = [['L3','AB']]
        self.assertEqual(self.rule.run_parser(),"L31 field under section L3 fails the max length (expected: 1) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L3','']]
        self.assertEqual(self.rule.run_parser(),"L31 field under section L3 fails the max length (expected: 1) validation, however it passes the data type (word_characters) validation.")

        self.rule.sentence_dict = [['L3','1']]
        self.assertEqual(self.rule.run_parser(),"L31 field under section L3 fails the data type (expected: word_characters) validation, however it passes the max length (1) validation.")

        self.rule.sentence_dict = [['L3','12']]
        self.assertEqual(self.rule.run_parser(),"L31 field under section L3 fails all the validation criteria.")

        print("[INFO] : L3 Test Casses Passed.\n") 


    def test_rule_based_parser_l4(self):
        print("[INFO] : Checking L4 Test Cases.\n")
        self.maxDiff = None

        # L4 test cases
        
        self.rule.sentence_dict = [['L4','A','123456']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under segment L4 passes all the validation criteria.")

        # L4 test cases for missing or additional sub_sections
        
        self.rule.sentence_dict = [['L4']]
        self.assertEqual(self.rule.run_parser(),"L41 field under section L4 is missing.L42 field under section L4 is missing.")

        self.rule.sentence_dict = [['L4','A']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 is missing.")

        self.rule.sentence_dict = [['L4','A','123456','']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under segment L4 passes all the validation criteria.L43 field under section L4 is missing in standard definition file.")

        # L41 test cases

        self.rule.sentence_dict = [['L4','AB','123456']]
        self.assertEqual(self.rule.run_parser(),"L41 field under section L4 fails the max length (expected: 1) validation, however it passes the data type (word_characters) validation.L42 field under segment L4 passes all the validation criteria.")

        self.rule.sentence_dict = [['L4','','123456']]
        self.assertEqual(self.rule.run_parser(),"L41 field under section L4 fails the max length (expected: 1) validation, however it passes the data type (word_characters) validation.L42 field under segment L4 passes all the validation criteria.")

        self.rule.sentence_dict = [['L4','1','123456']]
        self.assertEqual(self.rule.run_parser(),"L41 field under section L4 fails the data type (expected: word_characters) validation, however it passes the max length (1) validation.L42 field under segment L4 passes all the validation criteria.")

        self.rule.sentence_dict = [['L4','12','123456']]
        self.assertEqual(self.rule.run_parser(),"L41 field under section L4 fails all the validation criteria.L42 field under segment L4 passes all the validation criteria.")

        # L42 test cases

        self.rule.sentence_dict = [['L4','A','ABCDEF']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 fails the data type (expected: digits) validation, however it passes the max length (6) validation.")

        self.rule.sentence_dict = [['L4','A','1234567']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 fails the max length (expected: 6) validation, however it passes the data type (digits) validation.")

        self.rule.sentence_dict = [['L4','A','12345']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 fails the max length (expected: 6) validation, however it passes the data type (digits) validation.")

        self.rule.sentence_dict = [['L4','A','ABCDE']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 fails all the validation criteria.")

        self.rule.sentence_dict = [['L4','A','ABCDEFG']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 fails all the validation criteria.")

        self.rule.sentence_dict = [['L4','A','']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 fails all the validation criteria.")

        self.rule.sentence_dict = [['L4','A','ABC23']]
        self.assertEqual(self.rule.run_parser(),"L41 field under segment L4 passes all the validation criteria.L42 field under section L4 fails all the validation criteria.")

        print("[INFO] : L4 Test Casses Passed.\n") 


if __name__ == '__main__':
    unittest.main()