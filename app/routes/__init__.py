from flask import Flask

def init_app(app: Flask):

    from .categories_bp import bp_categories
    app.register_blueprint(bp_categories)
    from .tasks_bp import bp_tasks
    app.register_blueprint(bp_tasks)
    from .tasks_categories_bp import bp_tasks_categories
    app.register_blueprint(bp_tasks_categories)