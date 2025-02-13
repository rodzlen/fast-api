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
    fake_user_db[user.username]= {"username" : user.username, "password": hashed_password}
    return {"message": "User registered successfully"}

@app.post('/login')
def login(user :UserLogin):
    db_user = fake_user_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Inavalid username or password")
    access_token = create_access_token(data={"sub":user.username})
    return {"access_token":access_token, "token_type":"bearer"}



def get_current_user(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Invalid token')
        if not username in fake_user_db:
            raise HTTPException(status_code=401, detail='User not found')
        return fake_user_db[username]
    except JWTError:
        raise HTTPException(status_code=401, detail='invalid toekn')

@app.get('/profile')
def get_profile(current_user : dict = Depends(get_current_user)):
    return {"username":current_user['username']}