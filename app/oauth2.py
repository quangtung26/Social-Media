from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentals_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentals_exception

        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentals_exception
    
    return token_data


def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)
    