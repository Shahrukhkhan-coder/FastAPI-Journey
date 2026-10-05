from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_eligibility_pass():
    payload = {
        'income' : 60000,
        'age' : 25,
        'employment_status' : 'employed'
    }
    response = client.post('/loan_eligibility', json=payload)
    assert response.status_code == 200
    assert response.json() == {'Eligible' : True}



def test_eligibility_fail():
    payload = {
        'income' : 45000,
        'age' : 18,
        'employment_status' : 'unemployed'
    }
    response = client.post('/loan_eligibility', json=payload)
    assert response.status_code == 200
    assert response.json() == {'Eligible' : False}