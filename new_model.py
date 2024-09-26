
# Loading the necessary libraries 

import numpy as np
import pandas as pd

file_path = "question_database.csv"
data = pd.read_csv(file_path)

categories = ['Current Events', 'Fine Arts', 'Geography', 'History'
              , 'Literature', 'Mythology', 'Pop Culture', 'Religion',
              'Science', 'Social Science']

