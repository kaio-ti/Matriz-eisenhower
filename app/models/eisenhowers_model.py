from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from dataclasses import dataclass


@dataclass
class EisenhowersModel(db.Model):
    id: int
    type: str

    __tablename__ = 'eisenhowers'

    id = Column(Integer, primary_key=True)
    type = Column(String(100))
