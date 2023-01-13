from fastapi import FastAPI, Depends, Response, Request
import uvicorn
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from app import users, weight_logs, line
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from authware.oauth2passwordbearer import SECRET_KEY
from models.database import SessionLocal
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="RAKUKEN-API",
    middleware=[
        Middleware(SessionMiddleware, secret_key=SECRET_KEY)
    ],
)


templates = Jinja2Templates(directory='../frontend/build')
app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")

"""
BluePrintのRouter
"""
v1_prefix = "/api"
app.include_router(users.router, prefix=v1_prefix)
app.include_router(weight_logs.router, prefix=v1_prefix)
app.include_router(line.router, prefix=v1_prefix)

"""
ミドルウェアの設定
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

"""
Api - Handler
"""
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# ReactAppのホスティング
@app.get("/", response_class=HTMLResponse)
def react_app(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )

# 後ろでマウントしないとReactAppがホスティングできないため
app.mount("/", StaticFiles(directory="../frontend/build/"), name="public")

if __name__ == "__main__":
    uvicorn.run(app=app)