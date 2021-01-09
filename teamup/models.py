from flask import current_app
from teamup import login_manager, db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    db.reconnect()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user where userId = %s',(user_id,))
    res = cursor.fetchone()
    cursor.close()
    return User(userId = res[0],username = res[1],email=res[2],password=res[3])



class User(UserMixin):


    def __init__(self,email,username,password,userId = None):
        self.id = userId
        self.email = email
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"

class UserDetail():


    def __init__(self,userDetailId,userId,fullName=None,linkCV=None,linkGithub = None, linkPhoto=None,faculty=None, department=None,university=None,yearOfStudy=None,gpa=0,bio=None,likeCount=0):
        self.userDetailId = userDetailId
        self.userId = userId
        self.fullName = fullName
        self.linkCV = linkCV
        self.linkGithub = linkGithub
        self.linkPhoto = linkPhoto
        self.faculty = faculty
        self.department = department
        self.university = university
        self.yearOfStudy = yearOfStudy
        self.gpa = gpa
        self.bio = bio
        self.likeCount = likeCount


    def __repr__(self):
        return f"User('{self.id}', '{self.userId}')"

    
