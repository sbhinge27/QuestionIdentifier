import fitz  # PyMuPDF
import pandas as pd
import re

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        rect = page.rect
        if page_num == 0:
            height = 140
        else:
            height = 50
        clip = fitz.Rect(0, height, rect.width, rect.height-height)
        text += page.get_text(clip=clip)
    return text




# Function to clean up text by removing whitespace
def clean_text(text):
    lines = text.split('\n')
    
    # Define specific headers and footers to exclude
    excluded_patterns = [
        r'^Extra Question',
        r'Only read if moderator botches a question.'
        # Add more headers or footers if needed
    ]

    cleaned_lines = []
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace
        if not any(re.match(pattern, line) for pattern in excluded_patterns):
            cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines)

def merge_question_lines(lines):
    merged_lines = []
    buffer_line = ""
    question_number_pattern = re.compile(r'^\(\d+\)\s*$')

    for line in lines:
        line = line.strip()
        if question_number_pattern.match(line):
            buffer_line = line
        else:
            if buffer_line:
                merged_lines.append(buffer_line + " " + line)
                buffer_line = ""
            else:
                merged_lines.append(line)
    return merged_lines

# Path to the PDF file
pdf_path = 'qa.pdf'

# Extract text from the PDF
text = extract_text_from_pdf(pdf_path)

# Clean the extracted text to remove whitespace
cleaned_text = clean_text(text)

# Split the cleaned text into lines
lines = cleaned_text.split('\n')

# Merge lines where question numbers are on a separate line
lines = merge_question_lines(lines)

# Initialize lists to hold questions and answers
questions = []
answers = []

# Temporary variables to hold current question and answer
current_question = []
current_answer = []

# Regular expression to match question numbers at the beginning of the line
question_number_pattern = re.compile(r'^\(\d+\)')

# Process each line
for line in lines:
    line = line.strip()  # Remove leading and trailing whitespace
    if line.startswith("ANSWER:"):
        # If the line starts with "ANSWER:", it's an answer
        current_answer.append(line.replace("ANSWER:", "").strip())
        print(current_answer)
    elif question_number_pattern.match(line):
        # If the line starts with a question number, start a new question
        if current_question:
            questions.append(" ".join(current_question).strip())
            answers.append(" ".join(current_answer).strip())
            current_question = []
            current_answer = []
        line = question_number_pattern.sub("", line).strip()
        #print(line)
        current_question = [line]
        print(current_question)
    elif line:
        # Continue adding lines to the current question or answer
        if current_answer:
            current_answer.append(line)
            print(current_answer)
            #print(line)
        else:
            current_question.append(line)
            print(current_question)
            #print(line)

# Add any remaining question and answer if they exist
if current_question:
    questions.append(" ".join(current_question).strip())
if current_answer:
    answers.append(" ".join(current_answer).strip())

# Print lengths and samples of the lists for debugging
print(f"Number of questions: {len(questions)}")
print(f"Number of answers: {len(answers)}")
print("Sample questions:", questions[:5])
print("Sample answers:", answers[:5])

# Handle length mismatch
# If there are more questions than answers, add empty answers
if len(questions) > len(answers):
    answers.extend([""] * (len(questions) - len(answers)))
# If there are more answers than questions, truncate extra answers
elif len(answers) > len(questions):
    answers = answers[:len(questions)]

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Question': questions,
    'Answer': answers
})

# Save the DataFrame to a CSV file with UTF-8 encoding
df.to_csv('questions_answers.csv', index=False, encoding='utf-8')
