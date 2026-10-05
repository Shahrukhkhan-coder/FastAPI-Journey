from fastapi import FastAPI, Depends

app = FastAPI()

# dependency function

def get_db():
    db = {'Conection': 'Assume we have connection'}
    try:
        yield db
    finally:
        db.close()


@app.get('/index')
def home(db = Depends(get_db)):
    return {'db_status': db['connection']}