from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Start Server: uvicorn users:router --reload
router = APIRouter(prefix="/user",
                   tags=["/user"],
                   responses={404: {"msg":"Not found"}})

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

@router.get("/users")
async def users():
    return users_fake_db

# Path
@router.get("/{id}")
async def user(id: int):
    return search_user(id)
    
#Query
@router.get("/query/")
async def user_query(id: int):
    return search_user(id)

@router.post("", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail= "User alredy exists")
    else:
        users_fake_db.routerend(user)
        return(user)

@router.put("", response_model=User)
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index] = user
            found = True
    if not found:
        raise HTTPException(status_code=404, detail= "User not found")
    else:
        return user
    
@router.delete("{id}")
async def user(id : int):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found = True
        if not found:
           raise HTTPException(status_code=404, detail= "User not found")
        else:
            return {"msg": "User deleted"}


def search_user(id: int):
    users = filter(lambda user:user.id ==id, users_fake_db)
    try:
        return list(users)[0]
    except:
        return {"error":"User not found"}
    



