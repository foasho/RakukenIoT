from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from commons import common_func
from authware.oauth2passwordbearer import create_refresh_token, create_access_token, get_current_user, \
    create_device_token, create_password_hash
from models import schemas, database, models, crud
from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta
from conf.env import Env

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ユーザー情報の取得
@router.get("/user/{user_id}")
def retrieve_user(
        user_id: int,
        db=Depends(database.get_db),
        current_user=Depends(get_current_user)
):
    res = common_func.get_init_res()
    res["data"] = crud.get_user(db=db, user_id=user_id)
    res["success"] = True
    return schemas.RootResponse(**res)

# ユーザーの新規作成
@router.post("/user")
def create_user(
        body: schemas.UserCreate,
        db=Depends(database.get_db)
):
    res = common_func.get_init_res()
    db_user = crud.create_user(
        db=db,
        user=body
    )
    res["data"] = {
        "id": db_user.id,
        "username": db_user.username
    }
    res["success"] = True
    return schemas.RootResponse(**res)

# ユーザーの更新
@router.put("/user/{user_id}")
def update_user(
        user_id: int,
        body: schemas.UserUpdate,
        current_user = Depends(get_current_user),
        db=Depends(database.get_db),
):
    res = common_func.get_init_res()
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user.id == current_user.id:
        update_params = {}
        if body.new_password and db_user.password == body.old_password:
            update_params["password"] = body.new_password
        if body.email:
            update_params["email"] = body.email
        if body.username:
            update_params["username"] = body.username
        db_update_user = crud.update_user(
            db=db,
            user_id=user_id,
            user=update_params
        )
        if db_update_user:
            res["data"] = None
            res["success"] = True
    return schemas.RootResponse(**res)

"""
認証系
"""
## ログイン
@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    res = common_func.get_init_res()
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        if "@" in request.username:# メールアドレスでもログインできるようにする
            user = db.query(models.User).filter(models.User.email == request.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Invalid credentials'
            )
    if not user.password == create_password_hash(request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password'
        )
    res["data"] = {
        'access_token': create_access_token(data={'sub': user.username}),
        'refresh_token': create_refresh_token(data={'sub': user.username}),
        'device_token': create_device_token(data={'sub': user.username}),
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
    res["success"] = True
    return schemas.RootResponse(**res)

# リフレッシュトークンでアクセストークンを再取得
@router.post('/refresh')
def get_access_token_in_refresh(body: schemas.LoginRefresh, db: Session = Depends(database.get_db)):
    res = common_func.get_init_res()
    db_user = crud.get_user(db=db, user_id=body.user_id)
    if body.refresh_token == db_user.refresh_token:
        access_token = create_access_token(data={'sub': db_user.username})
        res["data"] = access_token
        res["success"] = True
    return schemas.RootResponse(**res)


# デバイス用アクセストークンを取得
@router.post('/device-token')
def get_device_access_token(
        current_user=Depends(get_current_user)
):
    res = common_func.get_init_res()
    res["data"] = create_device_token(data={'sub': current_user.username})
    res["success"] = True
    return schemas.RootResponse(**res)
