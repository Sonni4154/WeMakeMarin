from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Estimate(Base):
    __tablename__ = "estimates"
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric)
