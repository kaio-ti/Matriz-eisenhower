from app.exceptions.exceptions import UniqueViolation
from app.models.categories_model import CategoriesModel
from flask import current_app, request, jsonify


def create_category():
    try:

        data = request.json

        new_category = CategoriesModel(**data)

        current_app.db.session.add(new_category)
        current_app.db.session.commit()

        return jsonify(new_category), 201
 
    except UniqueViolation as e:
        return {"message": str(e)}, 409


def update_category(id):
    try:
        data = request.json

        return CategoriesModel.update_category(data, id)
    except UniqueViolation as e:
        return {"message": str(e)}, 409

def delete_category(id):
    return CategoriesModel.delete_category(id)
    