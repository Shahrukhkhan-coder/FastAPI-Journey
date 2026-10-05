from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Applicant(BaseModel):
    income : int
    age : int 
    employment_status : str


@app.post('/loan_eligibility')
def check_eligibility(applicant: Applicant):
        if (applicant.income >= 50000 ) and (applicant.age >= 21) and (applicant.employment_status == 'employed'):
            return {'Eligible' : True}
        else:
             return {'Eligible' : False}