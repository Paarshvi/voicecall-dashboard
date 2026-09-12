from sqlalchemy import Column, Integer, String

from database import Base


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    status = Column(String(20), nullable=False) 