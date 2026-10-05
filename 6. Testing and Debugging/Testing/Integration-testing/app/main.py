from fastapi import FastAPI
from pydantic import BaseModel
from app.logic import is_eligible_for_loan


app = FastAPI()


class Applicant(BaseModel):
    income : int
    age : int 
    employment_status : str


@app.post('/loan_eligibility')
def check_eligibility(applicant: Applicant):
    eligibility = is_eligible_for_loan(
        income = applicant.income,
        age = applicant.age,
        employment_status = applicant.employment_status
    )

    return {'Eligible' : eligibility}