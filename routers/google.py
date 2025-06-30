from fastapi import APIRouter

router = APIRouter()

@router.get("/docs")
def list_docs():
    return {"message": "List of Google Docs"}

@router.get("/sheets")
def list_sheets():
    return {"message": "List of Google Sheets"}

@router.get("/drive")
def list_drive():
    return {"message": "List of Google Drive files"}
