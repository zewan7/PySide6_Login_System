from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String, BLOB, DateTime
from sqlalchemy.orm import sessionmaker
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from config import config

engine = sqlalchemy.create_engine(config["db_url"])
Session = sessionmaker(bind=engine)

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(BLOB(255), nullable=False)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

# 自动创建所有表（如果数据库中已存在对应表，则会自动忽略不会重复创建）
Base.metadata.create_all(engine)
