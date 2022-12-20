from fastapi import APIRouter, Depends
from commons import common_func
from authware.oauth2passwordbearer import get_current_user
from models import schemas, database, crud

router = APIRouter()

@router.get("/weight-logs")
def get_weight_logs(
        current_user=Depends(get_current_user),
        db=Depends(database.get_db),
        skip=0,
        limit=5000,
        created_span: str = None
):
    res = common_func.get_init_res()
    res["data"] = crud.get_weight_logs(
        db=db,
        user_id=current_user.id,
        filter_params={
            "created_span": created_span
        },
        skip=skip,
        limit=limit
    )
    res["success"] = True
    return schemas.RootResponse(**res)

@router.post("/weight-log")
def create_weight_log(
        body: schemas.WeightLogCreate,
        current_user=Depends(get_current_user),
        db=Depends(database.get_db)
):
    res = common_func.get_init_res()
    res["data"] = crud.create_weight_log(db=db, weight_log=body)
    res["success"] = True
    return schemas.RootResponse(**res)

