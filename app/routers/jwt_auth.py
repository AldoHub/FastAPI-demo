from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

router = APIRouter(prefix="/jwt", tags=["jwt"])


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt/login")

#auth users entity
class User(BaseModel):
    id: int
    name: str
    
#extend user entity with password 
class UserInDB(User):
    hashed_password: str


usersDB = [
    UserInDB(id = 1, name="john@example.com", hashed_password="$2a$12$35DbylOxntzigklrlBN15ePyXqNN0rBjG6.1jiuJDoKPY9/KpMgXe"), #123456
    UserInDB(id = 2, name="mary@example.com", hashed_password="$2a$12$35DbylOxntzigklrlBN15ePyXqNN0rBjG6.1jiuJDoKPY9/KpMgXe"),
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

    #verify the password
    if pwd_context.verify(form_data.password, user.hashed_password):
        return {"access_token": user.name, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=403, detail="Invalid username or password")


#search user by id
def search_user(user_name: str):
    user = filter(lambda user: user.name == user_name, usersDB)
    try:
        return list(user)[0]
    except:
        raise HTTPException(status_code=400, detail="User not found")
    

