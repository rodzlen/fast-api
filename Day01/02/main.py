from fastapi import FastAPI

app = FastAPI()

@app.get('/users/{user_id}')
def users(user_id:int) -> dict:
    return {
        "user_id" : user_id,
        "status" : "active"
    }