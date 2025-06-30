from models import Customer, Estimate, Invoice
from database import SessionLocal

db = SessionLocal()

def list_all():
    print("Customers:")
    for c in db.query(Customer): print(c.id, c.name)
    print("Estimates:")
    for e in db.query(Estimate): print(e.id, e.amount)
    print("Invoices:")
    for i in db.query(Invoice): print(i.id, i.amount)

def run():
    print("Manual CLI (type 'exit' to quit)")
    while True:
        cmd = input(">> ").strip()
        if cmd == "exit":
            break
        try:
            exec(cmd)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
