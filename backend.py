from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Initialize the app
app = Flask(__name__)
CORS(app)

# Load the existing model and TF-IDF vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf.pkl', 'rb') as tfidf_file:
    tfidf = pickle.load(tfidf_file)

# Load the dataset (assuming it’s stored locally)
# This would ideally be replaced with a database in production
dataset = pd.read_csv('question_database.csv')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    question = data['question']

    # Transform the input question using the TF-IDF vectorizer
    question_tfidf = tfidf.transform([question])

    # Predict the category
    predicted_category = model.predict(question_tfidf)[0]

    # Return the predicted category
    return jsonify({'category': predicted_category})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    question = data['question']
    correct_category = data['category']
    approved = data['approved']

    # If the user has approved the prediction, we don't need to do anything
    if approved:
        return jsonify({'message': 'Thank you for your feedback!'})

    # If the user corrects the category, append it to the dataset
    global dataset
    new_entry = pd.DataFrame({'Question': [question], 'Category': [correct_category]})
    dataset = pd.concat([dataset, new_entry], ignore_index=True)

    # Retrain the model after adding the new entry
    retrain_model()

    return jsonify({'message': 'Thank you! The model has been updated with your feedback.'})

def retrain_model():
    global model, tfidf, dataset

    # Extract questions and categories from the updated dataset
    questions = dataset['Question']
    categories = dataset['Category']

    # Refit the TF-IDF vectorizer on the updated data
    X_tfidf = tfidf.fit_transform(questions)

    # Retrain the model
    model = MultinomialNB()
    model.fit(X_tfidf, categories)

    # Save the updated model and vectorizer
    with open('model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    with open('tfidf.pkl', 'wb') as tfidf_file:
        pickle.dump(tfidf, tfidf_file)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
