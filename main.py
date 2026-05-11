from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
  return {"message": "Hola"}

db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
  customer = Customer.model_validate(customer_data.model_dump())

  session.add(customer)
  session.commit()
  session.refresh(customer)

  return customer

@app.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
  return session.exec(select(Customer)).all()


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
  return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
  return invoice_data