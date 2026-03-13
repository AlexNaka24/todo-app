from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String)
    priority = Column(Integer, index=True)
    complete = Column(Boolean, index=True, default=False)