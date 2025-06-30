from fastapi import APIRouter

router = APIRouter()

@router.get("/forms")
def list_forms():
    return {"message": "List of Jotform forms"}
