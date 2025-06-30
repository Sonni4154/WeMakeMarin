
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Customer
import csv

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/help", response_class=HTMLResponse)
def help_page(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})

@router.get("/ui/customers", response_class=HTMLResponse)
def view_customers(request: Request, db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@router.post("/ui/customers", response_class=RedirectResponse)
def add_customer(name: str = Form(...), db: Session = Depends(get_db)):
    if len(name.strip()) < 2:
        return RedirectResponse(url="/ui/customers", status_code=303)
    db_customer = Customer(name=name.strip())
    db.add(db_customer)
    db.commit()
    return RedirectResponse(url="/ui/customers", status_code=303)

@router.post("/ui/customers/{customer_id}/edit", response_class=RedirectResponse)
def edit_customer(customer_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    customer = db.query(Customer).get(customer_id)
    if customer and len(name.strip()) > 1:
        customer.name = name.strip()
        db.commit()
    return RedirectResponse(url="/ui/customers", status_code=303)

@router.post("/ui/customers/{customer_id}/delete", response_class=RedirectResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).get(customer_id)
    if customer:
        db.delete(customer)
        db.commit()
    return RedirectResponse(url="/ui/customers", status_code=303)

@router.get("/logs/export", response_class=FileResponse)
def export_logs():
    input_path = "actions.log"
    output_path = "logs_export.csv"
    with open(input_path, "r") as infile, open(output_path, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Timestamp", "Level", "Message"])
        for line in infile:
            parts = line.strip().split(" - ", 2)
            if len(parts) == 3:
                writer.writerow(parts)
    return FileResponse(output_path, media_type="text/csv", filename="logs_export.csv")


from models import Estimate, Invoice

@router.get("/ui/estimates", response_class=HTMLResponse)
def view_estimates(request: Request, db: Session = Depends(get_db)):
    estimates = db.query(Estimate).all()
    return templates.TemplateResponse("estimates.html", {"request": request, "estimates": estimates})

@router.post("/ui/estimates", response_class=RedirectResponse)
def add_estimate(amount: float = Form(...), db: Session = Depends(get_db)):
    db_est = Estimate(amount=amount)
    db.add(db_est)
    db.commit()
    return RedirectResponse(url="/ui/estimates", status_code=303)

@router.post("/ui/estimates/{id}/edit", response_class=RedirectResponse)
def edit_estimate(id: int, amount: float = Form(...), db: Session = Depends(get_db)):
    item = db.query(Estimate).get(id)
    if item: item.amount = amount; db.commit()
    return RedirectResponse(url="/ui/estimates", status_code=303)

@router.post("/ui/estimates/{id}/delete", response_class=RedirectResponse)
def delete_estimate(id: int, db: Session = Depends(get_db)):
    item = db.query(Estimate).get(id)
    if item: db.delete(item); db.commit()
    return RedirectResponse(url="/ui/estimates", status_code=303)

@router.get("/ui/invoices", response_class=HTMLResponse)
def view_invoices(request: Request, db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    return templates.TemplateResponse("invoices.html", {"request": request, "invoices": invoices})

@router.post("/ui/invoices", response_class=RedirectResponse)
def add_invoice(amount: float = Form(...), db: Session = Depends(get_db)):
    db_inv = Invoice(amount=amount)
    db.add(db_inv)
    db.commit()
    return RedirectResponse(url="/ui/invoices", status_code=303)

@router.post("/ui/invoices/{id}/edit", response_class=RedirectResponse)
def edit_invoice(id: int, amount: float = Form(...), db: Session = Depends(get_db)):
    item = db.query(Invoice).get(id)
    if item: item.amount = amount; db.commit()
    return RedirectResponse(url="/ui/invoices", status_code=303)

@router.post("/ui/invoices/{id}/delete", response_class=RedirectResponse)
def delete_invoice(id: int, db: Session = Depends(get_db)):
    item = db.query(Invoice).get(id)
    if item: db.delete(item); db.commit()
    return RedirectResponse(url="/ui/invoices", status_code=303)
@router.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
