from app.exceptions.exceptions import InvalidImportanceOrUrgencyError, UniqueTaskError, UpdateImportanceOrUrgencyError
from app.models.tasks_categories_model import TasksCategoriesModel
from app.models.tasks_model import TasksModel
from app.models.categories_model import CategoriesModel
from flask import current_app, request


def create_task():
    data = request.json
    categories = []

    try:
        TasksModel.get_eisenhower(data)
        for category in data['categories']:
            if CategoriesModel.query.filter(CategoriesModel.name == category['name']).first() == None:
                current_app.db.session.add(CategoriesModel(name=category['name']))
                current_app.db.session.commit()
            categories.append(CategoriesModel.query.filter(CategoriesModel.name == category['name']).first())

        del data['categories']
        new_task = TasksModel(**data)
        current_app.db.session.add(new_task)
        current_app.db.session.commit()

        for category in categories:
            current_app.db.session.add(TasksCategoriesModel(task_id=new_task.id, category_id=category.id))
            current_app.db.session.commit()


        return{
            "id": new_task.id,
            "name": new_task.name,
            "description": new_task.description,
            "duration": new_task.duration,
            "eisenhower_classification": new_task.eisenhower_classification.type,
            "categories": [{"nome": category.name} for category in categories]
        }, 201

    except InvalidImportanceOrUrgencyError as e:
        return e.message, 404
    except UniqueTaskError:
        return {"message": "Task already in database"}, 409


def update_task(id):
    try:
        current_task = TasksModel.query.get(id)
        data = request.json
        data["eisenhower_id"] = 1
        if current_task == None:
            return {"msg": "Task not found"}, 404
        for key, value in data.items():
            if key == "urgency":
                TasksModel.update_urgency(data, current_task)
            if key == "importance":
                TasksModel.update_importance(data, current_task)
            setattr(current_task, key, value)
        current_app.db.session.add(current_task)
        current_app.db.session.commit()
        return {
                "id": current_task.id,
                "name": current_task.name,
                "description": current_task.description,
                "duration": current_task.duration,
                "eisenhower_classification": current_task.eisenhower_classification.type
            }, 200
    except UpdateImportanceOrUrgencyError:
        return {"msg": "Valores inválidos"}, 404

def delete_task(id):
    task = TasksModel.query.get(id)

    if task is None:
        return {"message": "Task not found"}

    current_app.db.session.delete(task)
    current_app.db.session.commit()

    return "", 204
    


