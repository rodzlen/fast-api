from asyncio import start_unix_server

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = '1234'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_user_db = {}
class UserRegister(BaseModel):
    username : str
    password : str
class UserLogin(BaseModel):
    username : str
    password : str
class Token(BaseModel):
    access_token : str
    token_type : str
class PatchProfile(BaseModel):
    username : str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


app = FastAPI()

@app.post('/register')
def register(user: UserRegister):
    if user.username in fake_user_db:
        raise HTTPException(status_code=400, detail='Username already exist')
    hashed_password = hash_password(user.password)
    fake_user_db[user.username]= {"username" : user.username, "password": hashed_password, "role":"user"}
    return {"message": "User registered successfully"}

@app.post('/register/admin')
def register_admin(user: UserRegister):
    if user.username in fake_user_db:
        raise HTTPException(status_code=400, detail='Username already exist')
    hashed_password = hash_password(user.password)
    fake_user_db[user.username]= {"username" : user.username, "password": hashed_password, "role":"admin"}
    return {"message": "User registered successfully"}

@app.post('/login')
def login(user :UserLogin):
    db_user = fake_user_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Inavalid username or password")
    if db_user['role']=='admin':
        access_token = create_access_token(data={"sub": user.username, "role":"admin"})
        return {"access_token": access_token, "token_type": "bearer", "role":"admin"}
    access_token = create_access_token(data={"sub":user.username})
    return {"access_token":access_token, "token_type":"bearer"}



def get_current_user(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        expire = payload.get('exp')
        if username is None:
            raise HTTPException(status_code=401, detail='Invalid token')
        if not username in fake_user_db:
            raise HTTPException(status_code=401, detail='User not found')
        return fake_user_db[username]
    except JWTError:
        raise HTTPException(status_code=401, detail='invalid toekn')

def check_access_token(token : str =Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    expire_timestamp =  payload.get('exp')

    expire_time = datetime.utcfromtimestamp(expire_timestamp) - datetime.utcnow()
    remaining_seconds = expire_time.total_seconds()

    if remaining_seconds > ACCESS_TOKEN_EXPIRE_MINUTES*60 :
        return {"status":200,"check_expire":remaining_seconds}
    return {"status":401,"check_expire":"Unauthorized"}


@app.get('/profile')
def get_profile(current_user : dict = Depends(get_current_user)):
    return {"username":current_user['username']}

@app.patch("/profile/{username}")
def patch_profile(username: str, profile_data: PatchProfile, current_user: dict = Depends(get_current_user)):
    # 일반 사용자는 자기 자신만 수정 가능, 관리자는 모든 사용자 수정 가능
    if current_user["username"] != username and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    # 존재하지 않는 사용자 예외 처리
    if username not in fake_user_db:
        raise HTTPException(status_code=404, detail="User not found")

    # 유저 정보 업데이트
    fake_user_db[username]["username"] = profile_data.username

    return {"username": fake_user_db[username]["username"]}


@app.get('/admin')
def admin_get(current_user: dict =  Depends(get_current_user)):
    if current_user['role'] == 'user':
        raise HTTPException(status_code=403, detail='Forbidden')
    else:
        print(fake_user_db)
        return {"status":200, "role":"admin"}

@app.get('/token-expiry')
def get_token_expiry(token : str = Depends(oauth2_scheme)):
    check_expiry = check_access_token(token)
    if check_expiry.get("check_expire") == "Unauthorized":
        raise HTTPException(status_code=check_expiry['status'], detail="Unauhorized")
    else:
        return {"status":check_expiry['status'], "expire_time":check_expiry['check_expire']}