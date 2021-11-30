# from app.models.tasks_model import TasksModel
from flask import current_app
from flask import jsonify, request
from app.models.categories_model import CategoriesModel

from app.models.tasks_categories_model import TasksCategoriesModel
from app.models.tasks_model import TasksModel

def get_tasks_categories():
    list = TasksCategoriesModel.query.all()

    return jsonify([{
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "tasks": [{
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "priority": task.eisehowers_classification.type
            } for task in category.result]
        } for category in list]), 200
