import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def get_async_items():
    await asyncio.sleep(2)
    return['ㅁㄴㅇ']