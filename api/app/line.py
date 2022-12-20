from fastapi import APIRouter, Depends, HTTPException, Request, Header
from models import schemas, database, crud
from sqlalchemy.orm.session import Session
from commons import common_func, message_masters
from authware.oauth2passwordbearer import get_current_user
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage
from conf.env import Env

router = APIRouter()
# LINEで利用する
line_bot_api = LineBotApi(Env("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(Env("LINE_CHANNEL_SECRET"))

# LINE連携コードの取得
@router.get("/line-code")
def get_linecode(
        db=Depends(database.get_db),
        current_user=Depends(get_current_user)
):
    res = common_func.get_init_res()
    db_users = crud.get_users(db=db)
    if not current_user.line_connect_code:
        all_user_line_codes = [db_user.line_connect_code for db_user in db_users if db_user.line_connect_code]
        line_code = common_func.random_integer_str(6, except_datas=all_user_line_codes)
        crud.update_user(
            db=db,
            user_id=current_user.id,
            user={
                "line_connect_code": str(line_code)
            }
        )
        res["data"] = str(line_code)
    else:
        res["data"] = str(current_user.line_connect_code)
    res["success"] = True
    return schemas.RootResponse(**res)

@router.post("/line/callback")
async def line_callback(request: Request, x_line_signature=Header(None)):

    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), x_line_signature)

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"


@handler.add(MessageEvent)
def handle_message(event):
    """
    LineBotから、
    受け取ったメッセージに従い返信メッセージを返答します。
    連携コード入力時、連携を行います。
    """
    db = database.SessionLocal()
    text = "すでに連携ずみです。"
    try:
        line_user_id = event.source.user_id
        db_already_user = crud.get_user_by_line_id(db=db, line_id=line_user_id)
        if not db_already_user:
            line_code = str(event.message.text)
            db_user = crud.get_user_by_line_code(db=db, line_code=str(line_code))
            if db_user == None:
                text = message_masters.Messages.LineNotCodeRegister
            else:
                if line_code == db_user.line_connect_code:
                    text = f"{db_user.username}さん\n" + message_masters.Messages.LineConnectSuccess
                    crud.update_user(
                        db=db,
                        user_id=db_user.id,
                        user={"line_id": line_user_id}
                    )
                else:
                    text = message_masters.Messages.LineDifferentCode
    except Exception as e:
        print(e)
        text = "想定外のエラーが発生しました。"
    finally:
        db.close()
    messages = TextSendMessage(text=text)
    line_bot_api.reply_message(event.reply_token, messages=messages)


# LINEメッセージで記録した体重を送信
@router.post("/line-weight")
def send_weight_line(
        body: schemas.DeviceWeightSend,
        current_user=Depends(get_current_user)
):
    res = common_func.get_init_res()
    if current_user.line_id:
        line_bot_api.push_message(
            to=current_user.line_id,
            messages=TextSendMessage(text=str(body.weight)+"kg")
        )
        res["success"] = True
    return schemas.RootResponse(**res)
