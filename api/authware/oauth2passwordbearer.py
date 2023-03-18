from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from models import database, crud, schemas, models
from passlib.context import CryptContext
from conf.env import Env

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme = HTTPBearer()

SECRET_KEY = Env("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 1時間
REFRESH_TOKEN_EXPIRE_MINUTES = 60*24*30 # 30日間
DEVICE_TOKEN_EXPIRE_YEAR = 90 # 90年※実質永遠
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
      to_encode = data.copy()
      expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      to_encode.update({"exp": expire, "access_type": "access"})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "access_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_device_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=365*DEVICE_TOKEN_EXPIRE_YEAR)
    to_encode.update({"exp": expire, "access_type": "device"})
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
        access_type: str = payload.get("access_type")
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
