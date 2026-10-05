import joblib
import pandas as pd

model = joblib.load('model/Mental_Health_Model.pkl')


def predict_output(require_data: dict):

    user_df = pd.DataFrame([require_data])

    prediction_output = model.predict(user_df)[0]

    return round(float(prediction_output),2)