# modules and imports
import pandas as pd
import sqlite3

# Extract | using pandas to read the csv files
extract = pd.read_csv("Student-Academic-Performance-Survey(Sheet1).csv", encoding='latin1')
og = pd.read_csv("Student-Academic-Performance-Survey(Sheet1).csv", encoding='latin1')
# print(extract)

# Transformtaion | renames, conversions, removal of invalid values & impossible numbers 

extract.rename(columns={
    'How many hours per week did you study on average? (please try and be as accurate as possible and just type the number. examples: 5, 9, 1, etc.)': 'hours_studied',
    'What is the percentage of lectures you attended? (please try and be as accurate as possible, just type the number. examples: 35, 60, 55, etc.)': 'attendance',
    'What was your prior cumulative before the semester that you took this class? (please try and be as accurate as possible. examples: 3.25, 3.00, 2.14, etc.)': 'prior_gpa',
    'Rate the class difficulty from (Easy = 1, Medium =\xa0\xa02, Hard = 3)\n': 'difficulty',
    'True or False, were you in any type of study group for the class?': 'in_studygroup',
    'What was your Test 1 score? (please try and be accurate. just type the number. examples: 80, 60, 42, etc.)': 'test1_score',
    'How confident were you when you took Test 1?\xa0': 'test1_confidence',
    'What was your Test 2\xa0score? (please try and be accurate. just type the number. examples: 80, 60, 42, etc.)': 'test2_score',
    'How confident were you when you took Test 2?\xa0': 'test2_confidence',
    'Final Grade in Class? (please try and be accurate. just type the number. examples: 70, 88, 61, etc.)': 'final_grade'
}, inplace=True)


# converting there values to numeric
extract['in_studygroup'] = extract['in_studygroup'].map({True: 1, False: 0})
extract['difficulty'] = extract['difficulty'].map({'1 = Easy': 1, '2 = Medium': 2, '3 = Hard':3})


#chceking adn updating values
extract['hours_studied'] = pd.to_numeric(extract['hours_studied'], errors = 'coerce')
extract['hours_studied'] = extract['hours_studied'].fillna(extract['hours_studied'].median())

extract['attendance'] = pd.to_numeric(extract['attendance'], errors='coerce')
extract['attendance'] = extract['attendance'].fillna(extract['attendance'].median())

extract['prior_gpa'] = pd.to_numeric(extract['prior_gpa'], errors='coerce')
extract['prior_gpa'] = extract['prior_gpa'].fillna(extract['prior_gpa'].median())

extract['difficulty'] = pd.to_numeric(extract['difficulty'], errors='coerce')
extract['difficulty'] = extract['difficulty'].fillna(extract['difficulty'].median())

extract['in_studygroup'] = pd.to_numeric(extract['in_studygroup'], errors='coerce')
extract['in_studygroup'] = extract['in_studygroup'].fillna(extract['in_studygroup'].median())

extract['test1_score'] = pd.to_numeric(extract['test1_score'], errors='coerce')
extract['test1_score'] = extract['test1_score'].fillna(extract['test1_score'].median())

extract['test1_confidence'] = pd.to_numeric(extract['test1_confidence'], errors='coerce')
extract['test1_confidence'] = extract['test1_confidence'].fillna(extract['test1_confidence'].median())

extract['test2_score'] = pd.to_numeric(extract['test2_score'], errors='coerce')
extract['test2_score'] = extract['test2_score'].fillna(extract['test2_score'].median())

extract['test2_confidence'] = pd.to_numeric(extract['test2_confidence'], errors='coerce')
extract['test2_confidence'] = extract['test2_confidence'].fillna(extract['test2_confidence'].median())

extract['final_grade'] = pd.to_numeric(extract['final_grade'], errors='coerce')
extract['final_grade'] = extract['final_grade'].fillna(extract['final_grade'].median())


# impossible numbers
extract = extract[extract['hours_studied'].between(0, 100)]
extract = extract[extract['attendance'].between(0, 100)]
extract = extract[extract['prior_gpa'].between(0.0, 4.0)]
extract = extract[extract['difficulty'].between(1, 3)]
extract = extract[extract['in_studygroup'].between(0, 1)]
extract = extract[extract['test1_score'].between(0, 100)]
extract = extract[extract['test1_confidence'].between(0, 10)]
extract = extract[extract['test2_score'].between(0, 100)]
extract = extract[extract['test2_confidence'].between(0, 10)]
extract = extract[extract['final_grade'].between(0, 100)]


# new columns
extract['avg_test_score'] = (extract['test1_score'] + extract['test2_score']) / 2
extract['avg_confidence'] = (extract['test1_confidence'] + extract['test2_confidence']) / 2
extract['passed'] = (extract['final_grade'] >= 60).astype(int)
extract['test1_weighted'] = extract['test1_score'] * (extract['test1_confidence'] / 10)
extract['test2_weighted'] = extract['test2_score'] * (extract['test2_confidence'] / 10)


extract = extract.drop(columns=['Id', 'Start time', 'Completion time', 'Email', 'Name'])

print(extract) 

# Load 
con = sqlite3.connect('data.db')
extract.to_sql('cleaned_data', con, if_exists='replace', index=False)
og.to_sql('original_data', con, if_exists='replace', index=False)
con.close()
