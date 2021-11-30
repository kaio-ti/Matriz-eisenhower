from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Text
from sqlalchemy.orm import validates, relationship
from flask import current_app
from app.exceptions.exceptions import InvalidCategoryError, UniqueViolation


@dataclass
class CategoriesModel(db.Model):
    id: int
    name: str
    description: str

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    task = relationship('TasksModel', secondary='tasks_categories', backref='categories')


    @validates('name')
    def validate(self, key, name):
        category = (
                CategoriesModel
                .query
                .filter(CategoriesModel.name==name)
                .one_or_none()
            )

        if category is not None:
            raise UniqueViolation("Categoria já existente")

        return name

    def update_category(data, id):

        category = CategoriesModel.query.filter(CategoriesModel.id==id).one_or_none()

        if category is None:
            return {"message": "Categoria não encontrada"}, 404

        for key, value in data.items():
            setattr(category, key, value)
        
        current_app.db.session.add(category)
        current_app.db.session.commit()

        return {"id": category.id, "name": category.name, "description": category.description}, 200

    def delete_category(id):

        category = CategoriesModel.query.get(id)

        if category is None:
            return {"message": "Category not found"}, 404

        current_app.db.session.delete(category)
        current_app.db.session.commit()

        return "", 204