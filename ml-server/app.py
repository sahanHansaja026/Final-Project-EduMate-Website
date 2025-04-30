from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Step 1: Train a very simple Sentiment Analysis model
# (In real life, you'd load a pretrained model)
training_data = [
    ("I love this course", "positive"),
    ("This is amazing", "positive"),
    ("Excellent work", "positive"),
    ("Very good experience", "positive"),
    ("I hate this", "negative"),
    ("This is terrible", "negative"),
    ("Very bad experience", "negative"),
    ("Worst course ever", "negative")
]

texts, labels = zip(*training_data)

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X_train, labels)

# Step 2: Define a prediction endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    messages = data.get("messages", [])

    # Vectorize input messages
    X_test = vectorizer.transform(messages)
    predictions = model.predict(X_test)

    # Build response
    result = [{"message": msg, "sentiment": pred} for msg, pred in zip(messages, predictions)]
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
