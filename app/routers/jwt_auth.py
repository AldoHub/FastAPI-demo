from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(prefix="/jwt", tags=["jwt"])

#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords

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


#receives the username and password as formdata and returns the access token
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form_data.username)

    #verify the password
    if pwd_context.verify(form_data.password, user.hashed_password):
        #return the access token
       
        #token expiration
        access_token_expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        #token details
        access_token_details = {
            "sub": user.name,
            "exp": access_token_expiration
        }

        access_token = jwt.encode(access_token_details, SECRET_KEY, algorithm=ALGORITHM)
        
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=403, detail="Invalid username or password")



async def authenticate_user(token: str = Depends(oauth2_scheme)):
    try:
        jwt_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = search_user(jwt_token["sub"])
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return User(id=user.id, name=user.name)
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid credentials")



async def get_current_user(user: User = Depends(authenticate_user)):
    user = search_user(user.name)
    if user:
        return user
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")



    
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
    

