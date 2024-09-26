import re
import csv

# Load the file
with open('imported_questions/data.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Pattern to remove question numbers like "1." or "(1)"
question_number_pattern = re.compile(r'^\(\d+\)|^\d+\.')

# Initialize variables
question = None
category = None
answer = None
data = []

# Loop through the lines and extract question, category, and answer
for i, line in enumerate(lines):
    if line.startswith("Question ID:"):
        # Reset variables when a new question ID is found
        question = None
        category = None
        answer = None
    elif re.match(r'^\d+\.|\(\d+\)', line):  # This line contains the question
        question = question_number_pattern.sub('', line).strip()
    elif line.startswith("<") and line.endswith(">"):
        category = line.strip("<>\n")
    elif line.startswith("ANSWER:"):
        answer = line.replace("ANSWER:", "").strip()
    
    # If all three components are found, add to the data list
    if question and answer:
        data.append([question, answer, "History"])
        question = None  # Reset for the next set of data

# Write to CSV
with open('sorted_questions.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Question', 'Answer', 'Category'])  # CSV headers
    csvwriter.writerows(data)

print("Data successfully written to 'sorted_questions.csv'.")
