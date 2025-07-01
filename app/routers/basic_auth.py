from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#auth users entity
class User(BaseModel):
    id: int
    name: str
    
#extend user entity with password 
class UserInDB(User):
    password: str

usersDB = [
    UserInDB(id = 1, name="john@example.com", password="123456"),
    UserInDB(id = 2, name="mary@example.com", password="123456"),
]


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if user:
        return user
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

#receives the username and password as formdata and returns the access token
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form_data.username)
    if user and user.password == form_data.password:
        return {"access_token": user.name, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=403, detail="Invalid username or password")

#returns the user information
@router.get("/users/me")
async def read_user_me(user: User = Depends(get_current_user)):
    return User(id=user.id, name=user.name)

#search user by id
def search_user(user_name: str):
    user = filter(lambda user: user.name == user_name, usersDB)
    try:
        return list(user)[0]
    except:
        raise HTTPException(status_code=400, detail="User not found")
    

