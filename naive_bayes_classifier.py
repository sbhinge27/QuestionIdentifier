import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# Load the dataset
file_path = "question_database.csv"
data = pd.read_csv(file_path)

# Extract the relevant columns
questions = data['Question']
categories = data['Category']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(questions, categories, test_size=0.2, random_state=42)

# Create a pipeline with TF-IDF Vectorizer and Naive Bayes Classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))
