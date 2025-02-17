from fastapi import FastAPI, HTTPException

app = FastAPI()

def get_div(a:int, b:int):
    if b == 0:
        raise HTTPException(status_code=400 , detail="0으로 나눌 수 없습니다")
    return a/b

@app.post('/math/devide')
def get_devide(a:int, b:int):
    return get_div(a,b)