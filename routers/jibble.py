from fastapi import APIRouter

router = APIRouter()

@router.get("/time-entries")
def list_time_entries():
    return {"message": "List of Jibble time entries"}
