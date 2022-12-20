from fastapi.security import OAuth2PasswordBearer, OAuth2, OAuth2AuthorizationCodeBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from models import database, crud, schemas, models
from conf.env import Env

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme = HTTPBearer()

SECRET_KEY = Env("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 60*24*30

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES, year: int = None):
      to_encode = data.copy()
      if year != None:
          expire = datetime.now() + timedelta(days=365*year)
      elif expires_delta:
          expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      else:
          expire = datetime.now() + timedelta(minutes=15)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = REFRESH_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_from_token(auth: HTTPAuthorizationCredentials, token_type: str, db: Session):
    """ tokenからユーザーを取得 """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Colud not validate credentials',
        headers={'WWW-Authenticate': "Bearer"}
    )
    # トークンをデコードしてペイロードを取得。有効期限と署名は自動で検証される。
    try:
        payload = jwt.decode(auth.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:#ここで期限切れを見てくれている
        raise credentials_exception

    # トークンタイプが一致することを確認
    if auth.scheme != token_type:
        raise credentials_exception

    # DBからユーザーを取得
    user = crud.get_user_by_username(db=db, username=payload['sub'])
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(auth = Depends(oauth2_scheme), db=Depends(database.get_db)):
    """アクセストークンからログイン中のユーザーを取得"""
    return get_current_user_from_token(auth, 'Bearer', db)
