from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "12345678"

    },
    "Casado2":{
        "username": "Casado2",
        "full_name": "Alejandro Casado 2",
        "email": "fakeemail2@fake.com",
        "disabled": True,
        "password": "12345678"

    }
}

def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    
def search_user(username: str):
    if username in user_db:
        return User(**user_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail= "Unauthorized", 
                            headers={"WWW-AUthenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= "Disabled User", 
                            headers={"WWW-AUthenticate": "Bearer"})
    else:
        return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_in_db = user_db.get(form.username)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User is not correct")
    else:
        user = search_user_db(username=form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Password is not correct")
    else:
        return {"access_token": user.username, "token_type": "bearer"}
    
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
