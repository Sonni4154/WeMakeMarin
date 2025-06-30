

from fastapi import APIRouter

from fastapi import APIRouter, HTTPException
from services.jotform_service import list_forms, form_submissions, convert_to_google

router = APIRouter()

@router.get("/forms")

def list_forms_endpoint():
    """List available Jotform forms via the API service."""

def list_forms():
    return {"message": "List of Jotform forms"}

  def list_forms_endpoint():

    try:
        return list_forms()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/forms/{form_id}/submissions")
def list_submissions(form_id: str):
    try:
        return form_submissions(form_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/forms/{form_id}/convert")
def convert_form(form_id: str):
    try:
        return convert_to_google(form_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
