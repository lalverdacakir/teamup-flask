from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
import re
from teamup import db,csrf
from teamup.models import User
from .utils import hash,verify
from .database import get_user,insert_user,get_user_detail,update_profile,get_user_interests,add_user_interest,delete_user_interest,get_like_count,check_like,remove_user_like,add_user_like
from teamup.teams.database import get_user_teams,get_admin_teams
from teamup.database import get_courses,get_deps, get_facs, get_unis,get_interests,add_dep,add_uni,add_fac
from .forms import LoginForm, RegisterForm, EditProfileForm, editInterestForm,dict_list_to_tuple_list

users = Blueprint('users',__name__)
@users.route("/register",methods = ['GET','POST'])
def register(): 
    msg = '' 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        query_user = get_user(username=form.username.data, email = form.email.data)
        count_res =len( query_user)
     
        if count_res != 0: 
            for res in query_user:
                if res['email'] == form.email.data:
                    msg = 'email exists'
                    break
                elif res['username'] == form.username.data:
                    msg = 'user exists'
                    break
                    
        else:
            hashed_password = hash(form.password.data)
            _dict = {"username": form.username.data, "email":form.email.data,"password":hashed_password}
            account = User(_dict)
            try:
                insert_user(account)
                flash('Your account has been created! You are now able to log in',category='success')
            except:
                flash("Failed to create account. Please try again",category='danger')
            return redirect(url_for('users.login'))
        
    parameters = {
        "msg": msg,
        "usr": current_user
    }
    return render_template('register.html', parameters = parameters,form=form)    

@users.route("/login", methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    msg = ''
    form = LoginForm(request.form)
    if form.validate_on_submit():
        account = get_user(username = form.username.data)
        if account:
            account = User(account[0])
            if(verify(account.password,form.password.data)):
                
                login_user(account,remember = True)
                
                next_page = request.args.get('next')
                
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', category='danger')
                msg = 'not verified'
        else:
             msg = 'not verified'

    parametes = {
        "msg": msg,
        "usr": current_user
    }
    return render_template('login.html',parameters = parametes,form = form)


@users.route("/logout")
@login_required 
def logout():
    if current_user.is_authenticated:
        logout_user()
    flash('Logged out','success')
    return redirect(url_for('main.home'))
  
@users.route("/profile/<string:username>")
def view_profile(username):
    
    account = get_user(username = username)
    if account:
        account_detail = get_user_detail(account[0]['userId'])
        likeCount = get_like_count(account[0]['userId'])
        current_user_liked = check_like(likedUserId=account[0]['userId'],userId=current_user.id)
        teams = get_user_teams(account[0]['userId'])
        admin_teams = get_admin_teams(account[0]['userId'])
        parameters = {
            "usr": current_user,
            "detail": account_detail,
            "likeCount": likeCount,
            "current_user_liked": current_user_liked,
            "teams":teams,
            "admin_teams":admin_teams
            
        }
        print(parameters)
        return render_template('profile.html',parameters = parameters)
    else:
        return redirect(url_for('main.home'))




@users.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    
    account_detail = get_user_detail(userId=current_user.id)
    par = {
        "usr": current_user,
        "detail": account_detail
    }
    form = EditProfileForm()
    if form.validate_on_submit():
        try:
            update_profile(user=current_user.id,form = form)
            flash('Your acount has been updated.',category='success')
        except:
            flash('Your account failed to update. Please try again later.',category='danger')
        
        return redirect(url_for('users.edit_profile'))
    

    photo_url = url_for('static',filename=account_detail['linkPhoto'])
    if(account_detail['linkCV']):
        cv_url = url_for('static',filename = account_detail['linkCV'])
    else:
        cv_url = ''
    form.fullName.default = account_detail['fullName']
    form.bio.default = account_detail['bio']
    form.yearOfStudy.default= account_detail['yearOfStudy']
    form.gpa.default = account_detail['gpa']
    form.university.default = account_detail['uniId']
    form.faculty.default = account_detail['facId']
    form.department.default = account_detail['depId']
    form.linkGithub.default = account_detail['linkGithub']
    form.process()
    
    
    
    return render_template('edit_profile.html',parameters = par,photo = photo_url,cv_url = cv_url,form = form)


@users.route('/add_university',methods=['POST'])
@login_required
def add_university():
  
    uniName = request.form['universityName']
    if(uniName):
        try:
            add_uni(uniName)
            flash('University created. After some time you will be able to select the newly added university',category='success')
        except:
            flash('Failed to add university. Please try again later',category='danger')
    return redirect(url_for('users.edit_profile'))

@users.route('/add_faculty',methods=['POST'])
@login_required
def add_faculty():
  
    facName = request.form['facultyName']
    if(facName):
        try:
            add_fac(facName)
            flash('Faculty created. After some time you will be able to select the newly added faculty',category='success')
        except:
            flash('Failed to add faculty. Please try again later',category='danger')
    return redirect(url_for('users.edit_profile'))

@users.route('/add_department',methods=['POST'])
@login_required
def add_department():
  
    depName = request.form['departmentName']
    if(depName):
        try:
            add_dep(depName)
            flash('Department created. After some time you will be able to select the newly added faculty',category='success')
        except:
            flash('Failed to add department. Please try again later',category='danger')
    return redirect(url_for('users.edit_profile'))


@users.route('/add_like/<int:userId>/<int:likedUserId>',methods=['POST'])
@login_required
def add_like(userId,likedUserId):
    if(current_user.id!=userId):
        return redirect(url_for('main.home'))
    try:
        account = get_user(userId = likedUserId)
        if(account):
            account = account[0]
            if(not check_like(likedUserId,userId)):
                
                try:
                    add_user_like(likedUserId,userId)
                    flash('User liked',category='success')
                except:
                    flash('Failed to like the user. Please try again later',category='danger')
            return redirect(url_for('users.view_profile',username =account['username']))
    except:
        flash('Faiuler','danger')
        return redirect(url_for('main.home'))

@users.route('/remove_like/<int:userId>/<int:likedUserId>',methods=['POST'])
@login_required
def remove_like(userId,likedUserId):
    if(current_user.id!=userId):
        return redirect(url_for('main.home'))
    try:
        account = get_user(userId = likedUserId)
        if(account):
            account = account[0]
            if(check_like(likedUserId,userId)):
                try:
                    remove_user_like(likedUserId,userId)
                    flash('Like removed',category='success')
                except:
                    flash('Failed to remove like. Please try again later',category='danger')
            return redirect(url_for('users.view_profile',username =account['username']))
    except:
        flash('Faiuler','danger')
        return redirect(url_for('main.home'))

