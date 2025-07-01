from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

#users entity
class User(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    url: str

#list of users
users = [
    User(id = 1, name="John", last_name="Doe", email="john@example.com", url="https://example.com/john"),
    User(id = 2,name="Mary", last_name="Smith", email="mary@example.com", url="https://example.com/mary"),
]

#return all users
@router.get("/users")
async def get_users():
    return users

#return user by id 
@router.get("/user/{user_id}")
async def get_user(user_id: int):
    return search_user(user_id)

#return user by id with a query parameter -- userquery/?user_id=1
@router.get("/userquery/")
async def get_user(user_id: int):
   return search_user(user_id)
    

#create a new user
@router.post("/user", response_model=User, status_code=201)
async def create_user(user: User):
    find_user = search_user(user.id)
    if type(find_user) == User:
       #raise an exception if the user already exists
       raise HttpException(status_code=400, detail="User already exists")
    else:
       users.append(user)
       return users
    

#update an user by id
@router.put("/user/{user_id}")
async def update_user(user_id: int, user: User):
    find_user = search_user(user_id)
    if type(find_user) == User:
        find_user.name = user.name
        find_user.last_name = user.last_name
        find_user.email = user.email
        find_user.url = user.url
        return find_user
    else:
        raise HttpException(status_code=400, detail="User not found")


@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    find_user = search_user(user_id)
    if type(find_user) == User:
        users.remove(find_user)
        return {"message": "User deleted"}
    else:    
        raise HttpException(status_code=404, detail="User not found")
#---- UTILS ----

#filter and return the user by id
def search_user(user_id: int):
    user = filter(lambda user: user.id == user_id, users)
    try:
        return list(user)[0]
    except:
        raise HttpException(status_code=400, detail="User not found")

