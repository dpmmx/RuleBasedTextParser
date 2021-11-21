# importing libraries
import json
import re
import os
import pandas as pd
import logging

class RuleBasedTextParser:
    '''
    ----------------------------------------------------------------------------------------------------
    This module provides a way to parse text file using Json Standard Defination file and generates summary files.
    ----------------------------------------------------------------------------------------------------
    
    Functions defined inside this Module:
    -------------------------------------
    load_input_file : Used for loading input text file into the Module.
    load_standard_definition_file : Used for loading Standard Definition Json file into the Module.
    load_error_file : Used for loading Error Json file into the Module.
    parse_text : Used for parsing the input file using a standard definition json file and generate a summary report.
    main : Used for excuting all required UDFs accroding to input and standard definition file.
    

    Return (output dir : parsed/):
    -------
    logfile.log : Provide step logs of the program.
    report.csv  : Provide the parsing reports into csv contains columns like 'Section', 'Sub-Section', 'Given DataType', 'Expected DataType', 'Given Length', 'Expected MaxLength', 'Error Code'.
    summary.txt : Provide parsing result i.e error code w.r.t each line.


    ----------------------------------------------------------------------------------------------------
    Author : Mukesh Maji
    ----------------------------------------------------------------------------------------------------
    '''
    
    # setting global variables
    global log_output_fullname, summary_output_fullname, rep_output_fullname, rule_line, parse_result_csv, summary, logger, msg
    
    # setting require output and logging file name
    log_output_name = 'logfile.log'
    summary_output_name = 'summary.txt'
    rep_output_name = 'report.csv'
    
    # setting output directory
    outdir = 'parsed/'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    # setting final output file paths
    log_output_fullname = os.path.join(outdir, log_output_name)
    summary_output_fullname = os.path.join(outdir, summary_output_name)
    rep_output_fullname = os.path.join(outdir, rep_output_name) 

    
    
    # defining variable used in class and UDFs
    msg = ""
    rule_line = ['L1','L2','L3','L4']
    error_codes = ['E01','E02','E03','E05','E06']
    parse_result_csv = pd.DataFrame(columns = ['Section','Sub-Section','Given DataType','Expected DataType','Given Length','Expected MaxLength','Error Code'])
    
   
    
    def __init__(self, input_file, separator, standard_definition_file, error_file):
        '''
        Inits RuleBasedTextParser Class
        
        Args:
        -----
        input_file : Input text file to Parsed or Can be None.
        separator : Variable (str) to separate input text lines into sub sections.
        standard_definition_file : Standard Definition file to be used for parsing.
        error_file : Error Reference file for Summary output.
        '''
        self.sentence_dict = []
        try:
            in_file = open(input_file, 'r')
            Lines = in_file.readlines()
            for line in Lines:
                 self.sentence_dict.append(line.rstrip("\n").split(separator))
            in_file.close()
        except:
            pass

        self.standard_definition_file = standard_definition_file
        self.error_file = error_file
        
    def load_standard_defination_file(self):
        '''
        Function used to load Standard Definition Json file.
        
        Attributes:
        -----------
        self.standard_definition_file : (Json File) Constructor attributes used. In this function self.standard_definition_file is used.
        
        Return:
        -----------
        Returns a list containing standard definition .
        '''
        try:
            with open(self.standard_definition_file) as json_data:
                standard_definition = json.load(json_data)
            json_data.close()
            return standard_definition
        except:
            raise FileNotFoundError("Standard Definition File not Loaded Properly. Check for File Name , Location.")
    
    def load_error_file(self):
        '''
        Function used to load Error Json file.
        
        Attributes:
        -----------
        self.error_file : (Json File) Constructor attributes used. In this function self.error_file is used.
        
        Note: This function is used to load Error Json file, but not used any where for Error handaling purpose.
        '''
        try:
            with open(self.error_file) as json_data:
                error = json.load(json_data)
            json_data.close()
            return error
        except:
            raise FileNotFoundError("Error File not Loaded Properly. Check for File Name , Location.")
    
    def parse_text(self, standard_definition, input_sentence, rule_string, sub_string_num):
        '''
        Function used to parse the input file using a standard definition json file and generate a summary report.
        
        Attributes:
        -----------
        standard_definition : Data Type : Dictionary , standard definition json file loaded into python dictionary.
        input_sentence : Data Type : int / float / str , sub sections of input text lines.
        rule_string : Data Type : str , values : {'L1', 'L2', 'L3', 'L4'}, Rule line as per Standard Definition json file.
        sub_string_num : Data Type : int, Sub Section Position in a Line.        
        '''
        global parse_result_csv, summary, msg_parse_sentence
               
        try:
            input_sentence = int(input_sentence)
        except:
            pass
        for i in range(len(rule_line)):
            if standard_definition[i]["key"] == rule_string:
                # Checking only digits [0-9], [A-Z], [a-z] and Space [' '] is in input sentences passed through input text file. If any other character is there in input text will result Error Code E06 , which is added by me.
                # Error Code E06 - {rule_string}{sub_string_num+1} field under section {rule_string} contains other than `0-9` and `A-Z` (both lower and uppercase) including space.
                if len(re.sub("[A-Za-z0-9 ]", '', str(input_sentence))) > 0:
                    parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num+1),'Given DataType':'others','Expected DataType':standard_definition[i]["sub_sections"][sub_string_num]["data_type"],'Given Length':len(str(input_sentence)),'Expected MaxLength':standard_definition[i]["sub_sections"][sub_string_num]["max_length"],'Error Code':'E06 (Added by Me)'},ignore_index=True)
                    summary.write(f"Error Code Added By Me {rule_string}{sub_string_num+1} field under section {rule_string} contains other than `0-9` and `A-Z` (both lower and uppercase) including space.\n")
                    msg_parse_sentence = f"Error Code Added By Me {rule_string}{sub_string_num+1} field under section {rule_string} contains other than `0-9` and `A-Z` (both lower and uppercase) including space."

                # Checking for E03 where max length failed but data type passed and input datatype is for digits
                elif (standard_definition[i]["sub_sections"][sub_string_num]["data_type"] == "digits" and (type(input_sentence) is int) == True) and ((len(str(input_sentence)) != standard_definition[i]["sub_sections"][sub_string_num]["max_length"])):
                    parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num+1),'Given DataType':'digits','Expected DataType':'digits','Given Length':len(str(input_sentence)),'Expected MaxLength':standard_definition[i]["sub_sections"][sub_string_num]["max_length"],'Error Code':'E03'},ignore_index=True)
                    summary.write(f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the max length (expected: {standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation, however it passes the data type ({standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation.\n")
                    msg_parse_sentence = f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the max length (expected: {standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation, however it passes the data type ({standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation."

                # Checking for E02 where max length passed but data type failed and input datatype is for digits
                elif (standard_definition[i]["sub_sections"][sub_string_num]["data_type"] == "digits" and (type(input_sentence) is int) == False) and ((len(str(input_sentence)) == standard_definition[i]["sub_sections"][sub_string_num]["max_length"])):
                    parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num+1),'Given DataType':'digits','Expected DataType':'digits','Given Length':len(str(input_sentence)),'Expected MaxLength':standard_definition[i]["sub_sections"][sub_string_num]["max_length"],'Error Code':'E02'},ignore_index=True)
                    summary.write(f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the data type (expected: {standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation, however it passes the max length ({standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation.\n")
                    msg_parse_sentence = f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the data type (expected: {standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation, however it passes the max length ({standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation."

                # Checking for E03 where max length failed but data type passed and input datatype is for word_characters
                elif (standard_definition[i]["sub_sections"][sub_string_num]["data_type"] == "word_characters" and (type(input_sentence) is str) == True) and ((len(str(input_sentence)) != standard_definition[i]["sub_sections"][sub_string_num]["max_length"])):
                    parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num+1),'Given DataType':'digits','Expected DataType':'digits','Given Length':len(str(input_sentence)),'Expected MaxLength':standard_definition[i]["sub_sections"][sub_string_num]["max_length"],'Error Code':'E03'},ignore_index=True)
                    summary.write(f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the max length (expected: {standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation, however it passes the data type ({standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation.\n")
                    msg_parse_sentence = f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the max length (expected: {standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation, however it passes the data type ({standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation."

                # Checking for E02 where max length passed but data type failed and input datatype is for word_characters
                elif (standard_definition[i]["sub_sections"][sub_string_num]["data_type"] == "word_characters" and (type(input_sentence) is str) == False) and ((len(str(input_sentence)) == standard_definition[i]["sub_sections"][sub_string_num]["max_length"])):
                    parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num+1),'Given DataType':'digits','Expected DataType':'digits','Given Length':len(str(input_sentence)),'Expected MaxLength':standard_definition[i]["sub_sections"][sub_string_num]["max_length"],'Error Code':'E02'},ignore_index=True)
                    summary.write(f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the data type (expected: {standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation, however it passes the max length ({standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation.\n")
                    msg_parse_sentence = f"{rule_string}{sub_string_num+1} field under section {rule_string} fails the data type (expected: {standard_definition[i]['sub_sections'][sub_string_num]['data_type']}) validation, however it passes the max length ({standard_definition[i]['sub_sections'][sub_string_num]['max_length']}) validation."

                # Checking for E04 where both max length and data type failed and input datatype is for both digits and word_characters
                elif ((standard_definition[i]["sub_sections"][sub_string_num]["data_type"] == "digits" and (type(input_sentence) is int) == False) and ((len(str(input_sentence)) != standard_definition[i]["sub_sections"][sub_string_num]["max_length"])) or (standard_definition[i]["sub_sections"][sub_string_num]["data_type"] == "word_characters" and (type(input_sentence) is str) == False) and ((len(str(input_sentence)) != standard_definition[i]["sub_sections"][sub_string_num]["max_length"]))):
                    parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num+1),'Given DataType':'digits','Expected DataType':'digits','Given Length':len(str(input_sentence)),'Expected MaxLength':standard_definition[i]["sub_sections"][sub_string_num]["max_length"],'Error Code':'E04'},ignore_index=True)
                    summary.write(f"{rule_string}{sub_string_num+1} field under section {rule_string} fails all the validation criteria.\n")
                    msg_parse_sentence = f"{rule_string}{sub_string_num+1} field under section {rule_string} fails all the validation criteria."

                # Checking for E01 where both max length and data type passed and input datatype is for both digits and word_characters
                else:
                    parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num+1),'Given DataType':'digits','Expected DataType':'digits','Given Length':len(str(input_sentence)),'Expected MaxLength':standard_definition[i]["sub_sections"][sub_string_num]["max_length"],'Error Code':'E01'},ignore_index=True)
                    summary.write(f"{rule_string}{sub_string_num+1} field under segment {rule_string} passes all the validation criteria.\n")
                    msg_parse_sentence = f"{rule_string}{sub_string_num+1} field under segment {rule_string} passes all the validation criteria."
        return msg_parse_sentence

    def run_parser(self):
        '''
        Function used to call the required User Defined Functions and and generate a summary report.        
        '''
        global parse_result_csv, rep_output_fullname, summary, msg
        parse_result_csv.iloc[0:0]
        msg = ""
        # configuring logger and setting the threshold of logger to DEBUG
        logging.basicConfig(filename=log_output_fullname, format='%(asctime)s %(message)s', filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # create summary output file with write permission
        summary = open(summary_output_fullname,"w")
        
        standard_definition = self.load_standard_defination_file()        # calling function to load Standard Definition File
        logger.info("[INFO] : Standard Definition Json File Loaded.")     # logging info
        
        # input_dict = self.load_input_file()                             # calling function to load input File
        if(self.sentence_dict == []):
            raise FileNotFoundError("Data Not Found! File not Loaded Properly. Check for File Name , Location or You can directly assign values to Modules' self.sentence_dict")
        else:
            input_dict = self.sentence_dict                               # calling function to load input File
                
        logger.info("[INFO] : Input Text File Loaded.")                   # logging info
        
        error_codes = self.load_error_file()                              # calling function to load error File
        logger.info("[INFO] : Error Json File Loaded.")                   # logging info
        
        for i in range(len(input_dict)):                                  # iterate through loaded input_dict
            logger.info(f"[INFO] : Traversing Line No {i}.")              # logging info
            for j in range (len(input_dict[i])):                          # iterate through sub sections 
                logger.info(f"[INFO] : Traversing Sub Sections No {j}.")  # logging info
                if j == 0 and input_dict[i][j] in rule_line:              # check whether it is first subsection and Rule Line is available in Standard Definition
                    rule_string = input_dict[i][j]                        # assigning Rule Line Number to rule_string variable                            
                    logger.info(f"[INFO] : Sub Sections No {j} Rule Line found : {rule_string}.")                    # logging info
                else:
                    try:                                                                                             # fails if input contains a sub section that not available in standard definition file
                        msg += self.parse_text(standard_definition, input_dict[i][j],rule_string,j-1)                # calling parse_text function
                    except IndexError as err:                                                                        # error raised if Rule Line or Sub Section not available in standard definition file
                        parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(j),'Given DataType':'','Expected DataType':'','Given Length':'','Expected MaxLength':'','Error Code':'E05'},ignore_index=True)
                        summary.write(f"{rule_string}{j} field under section {rule_string} is missing in standard definition file.\n")
                        msg += f"{rule_string}{j} field under section {rule_string} is missing in standard definition file."           # for unittesting
        
            # checking for any missing section in input file
            for k in range(len(standard_definition)):
                if standard_definition[k]["key"] == rule_string and len(standard_definition[k]["sub_sections"]) > j:
                    for m in range(len(standard_definition[k]["sub_sections"]) - j):
                        parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(j+m+1),'Given DataType':'','Expected DataType':'','Given Length':'','Expected MaxLength':'','Error Code':'E05'},ignore_index=True)
                        summary.write(f"{rule_string}{j+m+1} field under section {rule_string} is missing.\n")
                        msg += f"{rule_string}{j+m+1} field under section {rule_string} is missing."                  # for unittesting
        
        parse_result_csv.to_csv(rep_output_fullname, index=False)
        summary.close()
        logging.shutdown()
        return msg                                                        # for unittesting
