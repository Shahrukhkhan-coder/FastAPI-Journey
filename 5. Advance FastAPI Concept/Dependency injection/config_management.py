from fastapi import FastAPI, Depends

app = FastAPI()

class Settings():
    def __init__(self):
        self.api_key = 'The secret key'
        self.debug = True


def get_settings():
    return Settings()


@app.get('/config')
def get_config(settings : Settings = Depends(get_settings)):
    return {'API_key' : settings.api_key}