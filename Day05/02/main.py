from fastapi import FastAPI


app = FastAPI()

def multi(a : int, b : int):
    return {"result" : a*b}

@app.post('/math/multiply')
async def get_add(a:int, b:int):
    return get_add(a,b)

