from fastapi import APIRouter

router = APIRouter()

@router.get("/customers")
def get_customers():
    return {"message": "List of customers"}

@router.get("/estimates")
def get_estimates():
    return {"message": "List of estimates"}

@router.get("/invoices")
def get_invoices():
    return {"message": "List of invoices"}
