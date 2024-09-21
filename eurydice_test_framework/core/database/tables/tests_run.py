from datetime import datetime

from sqlalchemy import ARRAY, VARCHAR, Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TestsRun(Base):
    """Table config for tests runs"""
    __tablename__ = "tests_run"

    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, default=datetime.now())
    test = Column(VARCHAR)
    status = Column(VARCHAR)