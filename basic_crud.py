from fastapi import FastAPI
from pydantic import BaseModel

# start Server: uvicorn basic_crud:app --reload
app = FastAPI()

# User Model
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_fake_db = [User(id = 1, name="Alejandro", surname="Casado", url="casado.com", age = 27),
                 User(id = 2, name="Fernando", surname="Manzanares", url="fernando.com", age = 21),
                 User(id = 3, name="Oriana", surname="Moran", url="oriana.com", age = 27),]

@app.get("/users")
async def users():
    return users_fake_db

# Path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
#Query
@app.get("/userquery/")
async def user_query(id: int):
    return search_user(id)

@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error":"User alredy exists"}
    else:
        users_fake_db.append(user)
        return(user)

@app.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index] = user
            found = True
    if not found:
        return {"error": "User not found"}
    else:
        return user
    
@app.delete("/user/{id}")
async def user(id : int):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found = True
        if not found:
           return {"error": "User not found"}
        else:
            return {"msg": "User deleted"}


def search_user(id: int):
    users = filter(lambda user:user.id ==id, users_fake_db)
    try:
        return list(users)[0]
    except:
        return {"error":"User not found"}
    



