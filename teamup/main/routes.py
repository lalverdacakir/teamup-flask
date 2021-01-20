from flask import render_template, request, Blueprint,redirect,url_for
from teamup import login_manager
from flask_login import LoginManager,login_user, current_user, logout_user, login_required, UserMixin
import re
from flask_mail import Message
from teamup.teams.database import get_course_team_count,get_total_open_spots,get_accepting_team_count
from teamup import mail
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    parameters ={
        "usr":current_user,
        "course_team": get_course_team_count(),
        "accepting_team_count": get_accepting_team_count(),
        "total_open_spots": get_total_open_spots()
    }
    return render_template('main_page.html',parameters=parameters)

@main.route("/teams")
def teams():
    parameters ={
        "usr":current_user
    }
    if current_user.is_authenticated:
        
        return redirect(url_for('teams.main'))
    else:
        return redirect(url_for('main.home'))


@main.route("/contact", methods=['GET', 'POST'])
def contact():

    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'subject' in request.form and 'body' in request.form and 'first_name' in request.form and 'last_name' in request.form:
        email = request.form['email']
        subject = request.form['subject'] 
        body = request.form['body']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'email address invalid'
        
        elif not email or not subject or not body or not first_name or not last_name: 
            msg = 'form underfilled'
        else:
            subject = first_name + " " + last_name+ "    " + subject + "    --"+email 
            mail_msg = Message(body=body,sender = "lalverdac@gmail.com" ,subject = subject, recipients=["lalverdac@gmail.com"])
            mail.send(mail_msg)
            msg = 'message send'
    parameters = {
        "usr": current_user,
        "msg": msg
    }
    return render_template('contact.html',parameters=parameters  )
