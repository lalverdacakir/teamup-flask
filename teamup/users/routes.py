from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
import re
from teamup import db
from teamup.models import User, UserDetail
from .utils import hash,verify
from .database import get_user,insert_user,get_user_detail

users = Blueprint('users',__name__)
@users.route("/register",methods = ['GET','POST'])
def register(): 
    msg = '' 
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : 
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        
        #query_user = User.query.filter_by(username=username).all() + User.query.filter_by(email=email).all()
        query_user = get_user(username=username, email = email)
        count_res =len( query_user)

        if count_res != 0: 
            for res in query_user:
                if res[2] == email:
                    msg = 'email exists'
                    break
                elif res[1] == username:
                    msg = 'user exists'
                    break
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'email address invalid'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'username invalid'
        elif not username or not password or not email: 
            msg = 'form underfilled'
        else: 
            if len(password)<8:
                msg = 'short password'
            elif(confirm_password!=password):
                msg = 'doesnt match'
            else:
                hashed_password = hash(password)
                account = User(username=username, email =email,password = hashed_password)
                insert_user(account)
                msg = 'registered'
                return redirect(url_for('users.login'))

    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg,usr = current_user)


@users.route("/login", methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password'] 
        account = get_user(username = username)
        
        if account:
            account = account[0]
            account = User(userId = account[0],username = account[1],email = account[2],password = account[3])
            if(verify(account.password,password)):
                
                login_user(account,remember = True)
                
                next_page = request.args.get('next')
                
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
                msg = 'not verified'
        else:
             msg = 'not verified'

    return render_template('login.html',msg = msg,usr = current_user)

@users.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.home'))
  
@users.route("/profile/<string:username>")
def view_profile(username):
    
    account = get_user(username = username)
    if account:
        account = account[0]
        account = User(userId = account[0],username = account[1],email = account[2],password = account[3])
        account_detail = get_user_detail(account)
        if(account_detail):
            account_detail = account_detail[0]
            account_detail = UserDetail(userDetailId=account_detail[0],userId=account_detail[1],fullName=account_detail[2],linkCV=account_detail[3],linkGithub = account_detail[4], linkPhoto=account_detail[5],faculty=account_detail[6], department=account_detail[7],university=account_detail[8],yearOfStudy=account_detail[9],gpa=account_detail[10],bio=account_detail[11],likeCount=account_detail[12])
        return render_template('profile.html',usr = account,detail=account_detail,current_usr = current_user)
    else:
        return redirect(url_for('main.home'))

@users.route("/edit_profile")
def edit_profile():
    if current_user.is_authenticated:
        account_detail = get_user_detail(userId=current_user.id)
        return render_template('edit_profile',detail = account_detail[0])
    else:
        return  redirect(url_for('users.login'))
    

