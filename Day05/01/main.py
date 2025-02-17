from fastapi import FastAPI


app = FastAPI()

def add(a : int, b : int):
    return {'add' : a+b}

def sub(a:int , b: int):
    return {"sub": a-b}

@app.post('/add')
async def get_add(a:int, b:int):
    return get_add(a,b)


@app.post('/sub')
async def get_sub(a:int, b:int):
    return get_sub(a,b)

