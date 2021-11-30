from flask import Blueprint
from app.controllers.tasks_categories_controller import get_tasks_categories

bp_tasks_categories = Blueprint('bp_tasks_categories',  __name__)

bp_tasks_categories.get('/')(get_tasks_categories)