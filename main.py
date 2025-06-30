from fastapi import FastAPI
from routers.quickbooks import router as quickbooks_router

app = FastAPI(title="QuickBooks Sync App")

app.include_router(quickbooks_router, prefix="/qb", tags=["QuickBooks"])

from routers.google import router as google_router
from routers.gmail import router as gmail_router
from routers.jibble import router as jibble_router
from routers.jotform import router as jotform_router

app.include_router(google_router, prefix="/google", tags=["Google"])
app.include_router(gmail_router, prefix="/gmail", tags=["Gmail"])
app.include_router(jibble_router, prefix="/jibble", tags=["Jibble"])
app.include_router(jotform_router, prefix="/jotform", tags=["Jotform"])

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.ui import router as ui_router

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(ui_router)

from routers.auth import router as auth_router
from log_actions import log_action
from auth import get_current_user

app.include_router(auth_router)

@app.middleware("http")
async def log_middleware(request, call_next):
    user = request.headers.get("Authorization", "anonymous").replace("Bearer ", "")
    log_action(user, request.method, request.url.path)
    return await call_next(request)

from routers.google_auth import router as google_auth_router
app.include_router(google_auth_router)
