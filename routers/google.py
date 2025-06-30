from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.google_drive import list_files, download_file

router = APIRouter()

@router.get("/docs")
def list_docs():
    return {"message": "List of Google Docs"}

@router.get("/sheets")
def list_sheets():
    return {"message": "List of Google Sheets"}

@router.get("/drive")
def list_drive():
    try:
        return list_files()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/drive/download/{file_id}")
def drive_download(file_id: str):
    try:
        path = download_file(file_id, f"/tmp/{file_id}")
        return FileResponse(path, filename=file_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
