from flask import render_template, request, Blueprint
from teamup import login_manager
from flask_login import LoginManager,login_user, current_user, logout_user, login_required, UserMixin

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('ads.html',usr = current_user)
    else:
        return render_template('main_page.html',usr = current_user)