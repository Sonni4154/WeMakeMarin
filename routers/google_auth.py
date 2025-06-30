
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/login/google")
def login_google():
    # Placeholder: implement actual OAuth 2.0 flow
    return RedirectResponse(url="https://accounts.google.com/o/oauth2/auth")
