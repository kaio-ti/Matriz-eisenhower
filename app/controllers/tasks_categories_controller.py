from flask import jsonify
from app.models.categories_model import CategoriesModel

def get_tasks_categories():
    list = CategoriesModel.query.all()

    return jsonify([{
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "tasks": [{
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "priority": task.eisenhower_classification.type
            } for task in category.task]
        } for category in list]), 200
