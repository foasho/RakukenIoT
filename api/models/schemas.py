from typing import List, Union, Any, Optional
from pydantic import BaseModel

"""
認証系
"""
class Login(BaseModel):
    username: Optional[str]
    password: Optional[str]

class LoginRefresh(BaseModel):
    user_id: int
    refresh_token: str

"""
ユーザー処理
"""
class User(BaseModel):
    id: int
    description: Union[str, None] = None

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str]
    username: Optional[str]
    new_password: Optional[str]
    old_password: Optional[str]

"""
体重処理
"""
class WeightLogCreate(BaseModel):
    user_id: int
    value: float

class DeviceWeightSend(BaseModel):
    weight: float


## 共通レスポンス
class RootResponse(BaseModel):
    data: Any
    count: int = None
    messages: Any
    success: bool