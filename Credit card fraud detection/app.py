
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        final = np.array([features])
        prediction = model.predict(final)

        if prediction[0] == 1:
            output = 'Fraudulent Transaction 🚨'
        else:
            output = 'Normal Transaction ✅'

        return render_template('index.html', prediction_text=output)
    except:
        return "❌ Error in input. Please check your values!"

if __name__ == "__main__":
    app.run(debug=True)
