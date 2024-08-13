import fitz  # PyMuPDF
import pandas as pd
import re
import os

type_of_file = "nonUSGO"

# Regular expression to match question numbers at the beginning of the line
question_number_pattern = re.compile(r'^\(\d+\)|^\d+\.')
question_answer_pattern = re.compile('(?i)^answer:')

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        rect = page.rect
        if page_num == 0:
            if type_of_file == "nonUSGO":
                height = 50
            else:
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
        r'Only read if moderator botches a question.',
        r'Tossups'
        # Add more headers or footers if needed
    ]

    cleaned_lines = []
    q1_read = False
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace
        if not q1_read:
            if question_number_pattern.match(line):
                q1_read = True
                cleaned_lines.append(line)
        else:
                cleaned_lines.append(line)

        
    
    
    return "\n".join(cleaned_lines)

def merge_question_lines(lines):
    merged_lines = []
    buffer_line = ""
    question_number_pattern = re.compile(r'^\(\d+\)|^\d+\.')

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


pdf_name = input("Enter pdf name: ") + ".pdf"



# Path to the PDF file
pdf_path = 'imported_questions/' + pdf_name

# Extract text from the PDF
text = extract_text_from_pdf(pdf_path)
#print(text)

# Clean the extracted text to remove whitespace
cleaned_text = clean_text(text)
#print(cleaned_text)
# Split the cleaned text into lines
lines = cleaned_text.split('\n')

# Merge lines where question numbers are on a separate line
#lines = merge_question_lines(lines)

#for line in lines:
   # print(line)

# Initialize lists to hold questions and answers
questions = []
answers = []

# Temporary variables to hold current question and answer
current_question = []
current_answer = []



count = 1
# Process each line
for line in lines:
    line = line.strip()  # Remove leading and trailing whitespace
    #print(line)
    if count == 1:
        line = question_number_pattern.sub("", line).strip()
    count += 1
    if question_answer_pattern.match(line):
        # If the line starts with "ANSWER:", it's an answer
        #print(current_answer)
        #print(line)
        current_answer.append(re.sub("(?i)^ANSWER:", "", line))
        #print(current_answer)
    elif question_number_pattern.match(line) and current_answer:
        # If the line starts with a question number, start a new question
        if current_question:
            questions.append(" ".join(current_question).strip())
            answers.append(" ".join(current_answer).strip())
            current_question = []
            current_answer = []
        line = question_number_pattern.sub("", line).strip()
        # print(line)
        current_question = [line]
        #print(current_question)
    elif line:
        # Continue adding lines to the current question or answer
        if current_answer:
            current_answer.append(re.sub("^\d", "", line))
            #print(current_answer)
            #print(line)
        else:
            current_question.append(line)
          #  print(current_question)
            #print(line)

# Add any remaining question and answer if they exist
if current_question:
    questions.append(" ".join(current_question).strip())
if current_answer:
    answers.append(" ".join(current_answer).strip())

# Print lengths and samples of the lists for debugging
print(f"Number of questions: {len(questions)}")
print(f"Number of answers: {len(answers)}")
#print("Sample questions:", questions[0])
#print("Sample answers:", answers[0])

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

# Ensure the 'qa' folder exists
output_folder = 'qa'
os.makedirs(output_folder, exist_ok=True)

# Path to save the CSV file
csv_path = os.path.join(output_folder, pdf_name + '.csv')

# Save the DataFrame to a CSV file with UTF-8 encoding
df.to_csv(csv_path, index=False, encoding='utf-8')

print(f"CSV file saved to {csv_path}")
