from flask import Flask,render_template
from flask_login import LoginManager
from .config import Config
import mysql.connector
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

db = mysql.connector.MySQLConnection()
mail = Mail()
csrf = CSRFProtect()

app = Flask(__name__)
login_manager = LoginManager()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.connect(user=Config.MYSQL_USER,password = Config.MYSQL_PASSWORD,database=Config.MYSQL_DB)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'lalverdac@gmail.com',
    MAIL_PASSWORD = 'nazar2009nazar'
    )) 
    mail.init_app(app)
    csrf = CSRFProtect(app)
    from teamup.users.routes import users
    from teamup.main.routes import main
    from teamup.teams.routes import teams



    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(teams)
    @app.errorhandler(404)
    def resource_not_found(e):
        return render_template('404.html')
    return app