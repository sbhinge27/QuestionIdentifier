from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model and TF-IDF vectorizer (assuming they're saved as pickle files)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)

# Define a route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the input question from the request
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Preprocess the question using TF-IDF
    question_tfidf = tfidf.transform([question])
    
    # Predict the category
    predicted_category = model.predict(question_tfidf)[0]
    
    return jsonify({"category": predicted_category})

if __name__ == '__main__':
    app.run(debug=True)
