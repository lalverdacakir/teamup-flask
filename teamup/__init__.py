from flask import Flask
from flask_login import LoginManager
from .config import Config
import mysql.connector

db = mysql.connector.MySQLConnection()

login_manager = LoginManager()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.connect(user=Config.MYSQL_USER,password = Config.MYSQL_PASSWORD,database=Config.MYSQL_DB)
    login_manager.init_app(app)

    from teamup.users.routes import users
    from teamup.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(main)

    return app