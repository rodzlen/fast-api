import os
import shutil

from database import get_db, UserAct
from fastapi import FastAPI, Depends, BackgroundTasks, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
app = FastAPI()

def save_act(username: str, action:str, db:Session):
    new_activity = UserAct(username=username, action=action)
    db.add(new_activity)
    db.commit()


UPLOAD_DIR = "./upload"
async def save_file(file: UploadFile):
    """파일을 서버에 저장하는 함수"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # 파일 저장

    return file_path


@app.post('/upload-file/')
async def upload_file(  file: UploadFile,background_task : BackgroundTasks, db :Session = Depends(get_db), username : str=Form(...), action :str= Form(...)):
    background_task.add_task(save_act, username, action, db )
    file_path = await save_file(file)
    return {"message": "파일 업로드 중","file_path":file_path}

@app.get('/show-log')
def get_logs(db:Session= Depends(get_db)):
    logs = db.query(UserAct).all()
    return logs

@app.get('/show-log/{username}')
def get_user_logs(username:str, db :Session = Depends(get_db)):
    user_log = db.query(UserAct).filter(UserAct.username==username).all()
    if not user_log:
        raise HTTPException(status_code=404, detail='Not found user')
    return user_log