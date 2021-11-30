from flask import Blueprint
from app.controllers.categories_controller import create_category, update_category, delete_category


bp_categories = Blueprint('bp_categories',  __name__)

bp_categories.post('/category')(create_category)
bp_categories.patch('/category/<int:id>')(update_category)
bp_categories.delete('/category/<int:id>')(delete_category)