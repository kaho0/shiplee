import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from dotenv import load_dotenv
from model import Base, Order  


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


class OrderRequest(BaseModel):
    customer_name: str
    product_name: str
    price: float


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/order")
def create_order(order: OrderRequest, db: Session = Depends(get_db)):
    new_order = Order(
        customer_name=order.customer_name,
        product_name=order.product_name,
        price=order.price
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"status": "success", "order_id": new_order.id}


@app.get("/")
def read_root():
    return {"message": "Order Management API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)