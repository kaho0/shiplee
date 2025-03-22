import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

print("SQLAlchemy version:", sqlalchemy.__version__)

Base = declarative_base()
print("Base created:", Base)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

print("Order class defined")
print("Base metadata tables:", Base.metadata.tables.keys())