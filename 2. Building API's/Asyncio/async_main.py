import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get('/wait')
async def index():
    await asyncio.sleep(3)
    return {"Message" : "Finished Waiting!."}