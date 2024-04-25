from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 100
SECRET = "secretsauce"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


user_db = {
    "Casado":{
        "username": "Casado",
        "full_name": "Alejandro Casado",
        "email": "fakeemail@fake.com",
        "disabled": False,
        "password": "$2a$12$0DkcqwAyCIy9HbBna061keLmacM7/BC2Cppase5v6fZP7dpkZtzlS"

    },
    "Casado2":{
        "username": "Casado2",
        "full_name": "Alejandro Casado 2",
        "email": "fakeemail2@fake.com",
        "disabled": True,
        "password": "$2a$12$0DkcqwAyCIy9HbBna061keLmacM7/BC2Cppase5v6fZP7dpkZtzlS"

    }
}


def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    
def search_user(username: str):
    if username in user_db:
        return User(**user_db[username])

async def auth_user(token: str = Depends(oauth2)):
    
    exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                             detail= "Unauthorized", 
                             headers={"WWW-AUthenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
            
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= "Disabled User", 
                            headers={"WWW-AUthenticate": "Bearer"})
    else:
        return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_in_db = user_db.get(form.username)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User is not correct")
    else:
        user = search_user_db(username=form.username)
    
    if not crypt.verify(form.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail= "Password is not correct")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub": user.username,
                    "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}
   
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user