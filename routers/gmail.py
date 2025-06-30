from fastapi import APIRouter

router = APIRouter()

@router.get("/emails")
def list_emails():
    return {"message": "List of Gmail messages"}
