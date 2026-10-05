from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from schema.user_input import User_data
from model.predict import predict_output, model
from schema.predict_response import Prediction_response
from fastapi.staticfiles import StaticFiles


     
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve style.css and script.js as static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def serve_frontend():
    return FileResponse("static/index.html")

@app.get('/health')
def health_check():
    return {
        'Status':'OK',
        'model_loaded': model is not None
    }

@app.post('/Predict', response_model=Prediction_response)
def Predict_Health_Score(data: User_data):

    required_data = {
        'Age'                     : data.Age,
        'Gender'                  : data.Gender,
        'Country'                 : data.Country,
        'Academic_Level'          : data.Academic_Level,
        'Most_Used_Platform'      : data.Most_Used_Platform,
        'Purpose_Of_Use'          : data.Purpose_Of_Use,
        'Avg_Daily_Usage_Hours'   : data.Avg_Daily_Usage_Hours,
        'Daily_Unlocks'           : data.Daily_Unlocks,
        'Study_Hours'             : data.Study_Hours,
        'Physical_Activity_Hours' : data.Physical_Activity_Hours,
        'Sleep_Hours_Per_Night'   : data.Sleep_Hours_Per_Night,
        'Stress_Level'            : data.Stress_Level
    }


    try:

        prediction = predict_output(required_data)

        return JSONResponse(status_code=200, content={'Health_Score' : prediction})

    
    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))