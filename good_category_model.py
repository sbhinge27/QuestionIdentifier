import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# Load your dataset (questions and categories)
# Assuming the columns are 'Question' and 'Category'
file_path = 'question_database.csv'  # Update with your actual file path
data = pd.read_csv(file_path)

# Filter out the well-performing categories
good_categories = ['Geography', 'History', 'Literature', 'Science']

# Filter the dataset to include only these categories
filtered_data = data[data['Category'].isin(good_categories)]

# Extract the relevant columns
filtered_questions = filtered_data['Question']
filtered_categories = filtered_data['Category']

# Split the filtered dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(filtered_questions, filtered_categories, test_size=0.2, random_state=42)

# Step 1: Vectorize the text data using TF-IDF
tfidf = TfidfVectorizer()

# Fit the TF-IDF vectorizer on the training data and transform both train and test data
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Step 2: Train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Step 3: Make predictions on the test set
y_pred = model.predict(X_test_tfidf)

# Step 4: Evaluate the model's performance
print(classification_report(y_test, y_pred))

# Step 5: Save the model and TF-IDF vectorizer
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)