from sqlalchemy.orm import Session

from authware.oauth2passwordbearer import get_password_hash
from models import models, schemas
from sqlalchemy import desc, or_, func, asc

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).one_or_none()

def get_user_by_line_id(db: Session, line_id: str):
    return db.query(models.User).filter(models.User.line_id == line_id).one_or_none()

def get_user_by_line_code(db: Session, line_code: str):
    return db.query(models.User).filter(models.User.line_connect_code == str(line_code)).one_or_none()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict(exclude_unset=True))
    if db_user.password:
        db_user.password = get_password_hash(password=db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: dict):
    db_user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if db_user is None:
        return None
    for var, value in user.items():
        setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_weight_logs(db: Session, user_id: int, skip=0, limit=100, filter_params=None):
    filters = [models.WeightLog.user_id == user_id]
    if filter_params:
        if filter_params["created_span"]:
            dates = filter_params["created_span"].split(",")
            if len(dates) == 1:
                target_date = dates[0]
                if target_date[-1] == ">":
                    p = target_date.replace(">", "")
                    filters.append(models.WeightLog.created_at >= p)
                elif target_date[-1] == "<":
                    p = target_date.replace("<", "")
                    filters.append(models.WeightLog.created_at <= p)
                else:
                    filters.append(models.WeightLog.created_at <= target_date)
            if len(dates) == 2:
                d = []
                start_date = dates[0]
                end_date = dates[1]
                is_or = False
                if start_date[-1] == ">":
                    p = start_date.replace(">", "")
                    d.append(models.WeightLog.created_at >= p)
                elif start_date[-1] == "<":
                    p = start_date.replace("<", "")
                    d.append(models.WeightLog.created_at <= p)
                else:
                    is_or = True
                    d.append(models.WeightLog.created_at == start_date)
                if end_date[-1] == ">":
                    p = end_date.replace(">", "")
                    d.append(models.WeightLog.created_at >= p)
                elif end_date[-1] == "<":
                    p = end_date.replace("<", "")
                    d.append(models.WeightLog.created_at <= p)
                else:
                    is_or = True
                    d.append(models.WeightLog.created_at == end_date)
                if not is_or:
                    for df in d:
                        filters.append(df)
                else:
                    filters.append(
                        or_(d[0], d[1])
                    )
    return db.query(
        models.WeightLog
    ).filter(
        *filters
    ).order_by(
        # desc(models.WeightLog.created_at)
        asc(models.WeightLog.created_at)
    ).offset(skip).limit(limit).all()


def create_weight_log(db: Session, weight_log: schemas.WeightLogCreate):
    db_weight_create = models.WeightLog(**weight_log.dict(exclude_unset=True))
    db.add(db_weight_create)
    db.commit()
    db.refresh(db_weight_create)
    return db_weight_create