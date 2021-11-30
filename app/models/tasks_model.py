from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import backref, relationship, validates
from sqlalchemy.sql.sqltypes import Text
from app.configs.database import db
from dataclasses import dataclass

from app.exceptions.exceptions import InvalidImportanceOrUrgencyError, UniqueTaskError, UniqueViolation, UpdateImportanceOrUrgencyError
from app.models.categories_model import CategoriesModel


@dataclass
class TasksModel(db.Model):
    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    eisenhower_id: int

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100),nullable=False, unique=True)
    description = Column(Text, default="")
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)
    eisenhower_classification = relationship("EisenhowersModel", backref=backref('tasks', uselist=False), uselist=False)

    @validates('name')
    def validate(self, key, name):
        task = (
                TasksModel
                .query
                .filter(TasksModel.name==name)
                .one_or_none()
            )

        if task is not None:
            raise UniqueTaskError("Task já existente")

        return name

    @validates('importance')
    def verify_importance(self, key, importance):
      if importance != 1 and importance != 2:
        return [1,2]
      return importance

    @validates('urgency')
    def verify_urgency(self, key, urgency):
      if urgency != 1 and urgency != 2:
        return [1,2]
      return urgency

    def get_eisenhower(data):
        if data["importance"] == 1 and data["urgency"] == 1:
            data["eisenhower_id"] = 1
            return data["eisenhower_id"]
        if data["importance"] == 1 and data["urgency"] == 2:
            data["eisenhower_id"] = 2
            return data["eisenhower_id"]
        if data["importance"] == 2 and data["urgency"] == 1:
            data["eisenhower_id"] = 3
            return data["eisenhower_id"]
        if data["importance"] == 2 and data["urgency"] == 2:
            data["eisenhower_id"] = 4
            return data["eisenhower_id"]
        raise InvalidImportanceOrUrgencyError(data["urgency"], data["importance"])

    @staticmethod
    def update_importance(data, current_task):
        if data["importance"] == 1 and current_task.urgency == 1:
            data["eisenhower_id"] = 1
            return data["eisenhower_id"]
        if data["importance"] == 1 and current_task.urgency == 2:
            data["eisenhower_id"] = 2
            return data["eisenhower_id"]
        if data["importance"] == 2 and current_task.urgency == 1:
            data["eisenhower_id"] = 3
            return data["eisenhower_id"]
        if data["importance"] == 2 and current_task.urgency == 2:
            data["eisenhower_id"] = 4
            return data["eisenhower_id"]
        else:
            raise UpdateImportanceOrUrgencyError
    @staticmethod
    def update_urgency(data, current_task):
        if current_task.importance == 1 and data["urgency"] == 1:
            data["eisenhower_id"] = 1
            return data["eisenhower_id"]
        if current_task.importance == 1 and data["urgency"] == 2:
            data["eisenhower_id"] = 2
            return data["eisenhower_id"]
        if current_task.importance == 2 and data["urgency"] == 1:
            data["eisenhower_id"] = 3
            return data["eisenhower_id"]
        if current_task.importance == 2 and data["urgency"] == 2:
            data["eisenhower_id"] = 4
            return data["eisenhower_id"]
        else:
            raise UpdateImportanceOrUrgencyError