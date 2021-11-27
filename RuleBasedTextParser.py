# importing libraries
import json
import re
import os
import pandas as pd
import logging
import time

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

    '''
    
    # setting global variables
    global log_output_fullname, summary_output_fullname, rep_output_fullname, rule_line, parse_result_csv, summary, logger, msg, outdir
    
    # setting require output and logging file name
    log_output_name = 'logfile.log'
    summary_output_name = 'summary.txt'
    # rep_output_name = 'report'+time.strftime("%Y%m%d-%H%M%S")+'.csv'
    
    # setting output directory
    outdir = 'parsed/'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    # setting final output file paths
    log_output_fullname = os.path.join(outdir, log_output_name)
    summary_output_fullname = os.path.join(outdir, summary_output_name) 

    
    
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
    
    def write_error(self, rule_string, sub_string_num, given_datatype, expected_datatype, given_length, expected_length, error_code):
        '''
        Function used to Write Error Ouput in Output files.
        
        Attributes:
        -----------
        rrule_string : Data Type : str , values : {'L1', 'L2', 'L3', 'L4'}, Rule line as per Standard Definition json file.
        sub_string_num : Data Type : int, Sub Section Position in a Line.   
        given_datatype : Data Type : str
        expected_datatype : Data Type : str
        given_length : Data Type : int
        expected_length : Data Type : int
        error_code :  Data Type : str
        '''
        global parse_result_csv, summary, msg_parse_sentence

        parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(sub_string_num),'Given DataType':given_datatype,'Expected DataType':expected_datatype,'Given Length':given_length,'Expected MaxLength':expected_length,'Error Code': error_code},ignore_index=True)
        
        if(error_code == 'E01'):
            summary.write(f"{rule_string}{sub_string_num} field under segment {rule_string} passes all the validation criteria.\n")
            msg_parse_sentence = f"{rule_string}{sub_string_num} field under segment {rule_string} passes all the validation criteria."   # for unittesting
        elif(error_code == 'E02'):
            summary.write(f"{rule_string}{sub_string_num} field under section {rule_string} fails the data type (expected: {expected_datatype}) validation, however it passes the max length ({expected_length}) validation.\n")
            msg_parse_sentence = f"{rule_string}{sub_string_num} field under section {rule_string} fails the data type (expected: {expected_datatype}) validation, however it passes the max length ({expected_length}) validation."   # for unittesting
        elif(error_code == 'E03'):
            summary.write(f"{rule_string}{sub_string_num} field under section {rule_string} fails the max length (expected: {expected_length}) validation, however it passes the data type ({expected_datatype}) validation.\n")
            msg_parse_sentence = f"{rule_string}{sub_string_num} field under section {rule_string} fails the max length (expected: {expected_length}) validation, however it passes the data type ({expected_datatype}) validation."   # for unittesting
        elif(error_code == 'E04'):
            summary.write(f"{rule_string}{sub_string_num} field under section {rule_string} fails all the validation criteria.\n")
            msg_parse_sentence = f"{rule_string}{sub_string_num} field under section {rule_string} fails all the validation criteria."   # for unittesting
        elif(error_code == 'E05'):
            summary.write(f"{rule_string}{sub_string_num} field under section {rule_string} is missing.\n")
            msg_parse_sentence += f"{rule_string}{sub_string_num} field under section {rule_string} is missing."   # for unittesting
        return msg_parse_sentence

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
        feeded_datatype = ""
        feeded_max_length = 0


        try:
            input_sentence = int(input_sentence)
        except:
            pass
        for i in range(len(rule_line)):
            if standard_definition[i]["key"] == rule_string:

                # checking for datatype of input sentence
                if len(re.sub("[A-Za-z0-9 ]", '', str(input_sentence))) > 0:
                    feeded_datatype = 'others'
                elif (type(input_sentence) is int) == True :
                    feeded_datatype = 'digits'
                else:
                    feeded_datatype = 'word_characters'
                
                # if input sentence is not null
                if len(str(input_sentence)) > 0:
                    feeded_max_length = len(str(input_sentence))
                    # E03 Error Code checking 
                    if(standard_definition[i]["sub_sections"][sub_string_num]["data_type"] == feeded_datatype) and (feeded_max_length > standard_definition[i]["sub_sections"][sub_string_num]["max_length"]):
                        msg_parse_sentence = self.write_error(rule_string, sub_string_num+1, feeded_datatype, standard_definition[i]["sub_sections"][sub_string_num]["data_type"], feeded_max_length, standard_definition[i]["sub_sections"][sub_string_num]["max_length"], 'E03')
                    # E02 Error Code checking
                    elif(standard_definition[i]["sub_sections"][sub_string_num]["data_type"] != feeded_datatype) and (feeded_max_length <= standard_definition[i]["sub_sections"][sub_string_num]["max_length"]):
                        msg_parse_sentence = self.write_error(rule_string, sub_string_num+1, feeded_datatype, standard_definition[i]["sub_sections"][sub_string_num]["data_type"], feeded_max_length, standard_definition[i]["sub_sections"][sub_string_num]["max_length"], 'E02')
                    # E04 Error Code checking
                    elif(standard_definition[i]["sub_sections"][sub_string_num]["data_type"] != feeded_datatype) and (feeded_max_length > standard_definition[i]["sub_sections"][sub_string_num]["max_length"]):
                        msg_parse_sentence = self.write_error(rule_string, sub_string_num+1, feeded_datatype, standard_definition[i]["sub_sections"][sub_string_num]["data_type"], feeded_max_length, standard_definition[i]["sub_sections"][sub_string_num]["max_length"], 'E04')
                    # if all okay E01 Error Code
                    else:
                        msg_parse_sentence = self.write_error(rule_string, sub_string_num+1, feeded_datatype, standard_definition[i]["sub_sections"][sub_string_num]["data_type"], feeded_max_length, standard_definition[i]["sub_sections"][sub_string_num]["max_length"], 'E01')
                # if input sentence is null E04
                else:
                    msg_parse_sentence = self.write_error(rule_string, sub_string_num+1, '', standard_definition[i]["sub_sections"][sub_string_num]["data_type"], '', standard_definition[i]["sub_sections"][sub_string_num]["max_length"], 'E04')
                
                
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
                        # parse_result_csv = parse_result_csv.append({'Section':rule_string,'Sub-Section':rule_string+str(j),'Given DataType':'','Expected DataType':'','Given Length':'','Expected MaxLength':'','Error Code':'E05'},ignore_index=True)
                        # summary.write(f"{rule_string}{j} field under section {rule_string} is missing in standard definition file.\n")
                        # msg += f"{rule_string}{j} field under section {rule_string} is missing in standard definition file."           # for unittesting
                        pass
        
            # checking for any missing section in input file - E05
            for k in range(len(standard_definition)):
                if standard_definition[k]["key"] == rule_string and len(standard_definition[k]["sub_sections"]) > j:
                    for m in range(len(standard_definition[k]["sub_sections"]) - j):
                        msg += self.write_error(rule_string, j+m+1, '', standard_definition[k]["sub_sections"][j+m]["data_type"], '', standard_definition[k]["sub_sections"][j+m]["max_length"], 'E05')
        
        rep_output_name = 'report'+time.strftime("%Y%m%d-%H%M%S")+'.csv'
        rep_output_fullname = os.path.join(outdir, rep_output_name)
        parse_result_csv.to_csv(rep_output_fullname, index=False)
        summary.close()
        logging.shutdown()
        return msg                                                        # for unittesting
