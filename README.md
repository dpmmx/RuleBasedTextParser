# RuleBasedTextParser
Parses input text file, using the provided standard definition (Json File) and generate a summary report in text and csv.


## Tech Stack:
Language: Python

## Version Details: 
python   --> 3.8.12
json     --> 2.0.9
re       --> 2.2.1
pandas   --> 1.3.4
logging  --> 0.5.1.2

## Standard Definition Json File:

Standard Rules to parse a input text file. It uses the following structure and Parsing Rules.

- -> key (LX)
- -> sub_sections (contains the following)
- ---------------> key (sub_section: LXY)
- ---------------> data_type ('digits' / 'word_characters')
- ---------------> max_length (data type : int)


## Error Json File:

E01: "message_template": "LXY field under segment LX passes all the validation criteria."
E02: "message_template": "LXY field under section LX fails the data type (expected: {data_type}) validation, however it passes the max length ({max_length}) validation"
E03: "message_template": "LXY field under section LX fails the max length (expected: {data_type}) validation, however it passes the data type ({data_type}) validation"
E04: "message_template": "LXY field under section LX fails all the validation criteria."
E05: "message_template": "LXY field under section LX is missing."

E06: "message_template": "LXY field under section LX contains other than `0-9` and `A-Z` (both lower and uppercase) including space."
E07: "message_template": "LXY field under section LX is missing in standard definition file."


## Input File:

Input file should contains multiple sections which are separated by new line (`\n`) character, and the sections are sub-separated by ampersand character (`&`)

	```
	L1&99&&A
	L4&9
	```

## Code Snippet:

- >>> from RuleBasedTextParser import RuleBasedTextParser
- >>> test = RuleBasedTextParser('input_file_2.txt','&','standard_definition.json','error_codes.json')
- >>> test.run_parser()
'L11 field under section L1 fails the max length (expected: 1) validation, however it passes the data type (digits) validation.L12 field under section L1 fails the max length (expected: 3) validation, however it passes the data type (word_characters) validation.L13 field under section L1 fails the max length (expected: 2) validation, however it passes the data type (word_characters) validation.L41 field under section L4 fails the data type (expected: word_characters) validation, however it passes the max length (1) validation.L42 field under section L4 is missing.'

And also modify test.sentence_dict, which can be used to do unit testing

- >>>test.sentence_dict = [['L1','1','ABC','AB']]
- >>>test.run_parser()
'L11 field under segment L1 passes all the validation criteria.L12 field under segment L1 passes all the validation criteria.L13 field under segment L1 passes all the validation criteria.'

## Some Rules:

1. digits are only numbers between `0-9` and word characters are english letters between `A-Z` (both lower and uppercase) including space.
2. Empty spaces count towards the length of the field, e.g. length of `A A` is 3. 
3. Used `others` as the datatype for datatypes other than `digits` and `word_characters`.

## Unit Testing File

Unit testing file (test_RuleBasedTextParser.py) contains almost all the possible outcome from the Module.
