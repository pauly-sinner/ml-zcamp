import pickle

from flask import Flask
from flask import request
from flask import jsonify


#model_file = 'model1.bin'

with open('model2.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary
    model = pickle.load(f_in)
with open('dv.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary
    dv = pickle.load(f_in)

app = Flask('proba')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    churn = y_pred >= 0.5

    result = {
        'churn_probability': float(y_pred),
        'churn': bool(churn)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)