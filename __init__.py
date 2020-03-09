from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from .user import User
        return User.query.get(int(user_id))

    return app

if __name__ == '__main__':
    create_app()