from teamup import db,app
from ..models import User
from flask import jsonify
from datetime import date
import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
def get_user(username=None,email=None,userId=None):

    cursor = db.cursor(dictionary=True)
    values = ()
    sql = 'SELECT * FROM user '
    if (username or email or userId):
        sql = sql + 'WHERE '
    if username:
        sql = sql + 'username = %s '
        values = values + (username,)
    if email:
        if username:
            sql = sql + 'OR '
        sql = sql + 'email = %s '
        values = values + (email,)
    if userId:
        if username or email:
            sql = sql + 'OR '
        sql = sql + 'userId = %s '
        values = values + (userId,)

    cursor.execute(sql,values)
    res = cursor.fetchall()
    cursor.close()
    print(res)  
    return res
def get_user_detail(userId):
    sql = '''SELECT user.username, user.email, userdetail.*,university.uniName,department.depName,faculty.facName
            FROM userdetail
            LEFT JOIN user  ON user.userId = userdetail.userId
            INNER JOIN university on university.uniId = userdetail.uniId
            INNER JOIN department on department.depId = userdetail.depId
            INNER JOIN faculty on faculty.facId = userdetail.facId
            WHERE user.userId = %s;'''
    cursor = db.cursor(dictionary=True)
    
    cursor.execute(sql,(userId,))
    res = cursor.fetchone()
    cursor.close()
    return res


def insert_user(user):
    cursor = db.cursor(dictionary=True)

    sql = 'INSERT INTO user(username,email,password) VALUES(%s,%s,%s)'

    values = (user.username,user.email,user.password)
    cursor.execute(sql,values)
    db.commit()
    user.id= cursor.lastrowid
    sql = 'INSERT INTO userdetail(userId) VALUES(%s)'
    values = (user.id,)
    cursor.execute(sql,values)
    db.commit()
    cursor.close()
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(form_picture.filename)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_img', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_CV(form_CV):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(form_CV.filename)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    path = os.path.join(app.root_path, 'static/files/CV', picture_fn)
    
    output_size = (125, 125)
   
    form_CV.save(path)

    return picture_fn
def update_profile(user,form):
    cursor = db.cursor(dictionary=True)
    path_CV = ''
    path_p = 'img/profile_img/'
    if(form.linkPhoto.data):
        path_p += save_picture(form.linkPhoto.data)
    else:
        path_p += 'dummy.jpg'
    if(form.linkCV.data):
        path_CV =  'files/CV/' + save_CV(form.linkCV.data)
    
        
    values = (form.fullName.data,form.bio.data,form.university.data,form.faculty.data,form.department.data,form.yearOfStudy.data,form.gpa.data,path_p,path_CV,form.linkGithub.data,user)
    sql = '''update userdetail
        set fullName = %s,
        bio = %s,
        uniId = %s,
        facId = %s,
        depId = %s,
        yearOfStudy = %s,
        gpa = %s,
        linkPhoto = %s,
        linkCV = %s,
        linkGithub = %s
        where userId = %s'''
  

    cursor.execute(sql,values)
    db.commit()
    cursor.close()
    

def get_likes(likedUser=None,user=None):
    cursor = db.cursor(dictionary=True)
    values = ()
    sql = 'select * from likes'
    if(likedUser or user):
        sql+='where '
    if(likedUser):
        sql += 'likedUserId = %s '
        values += (likedUser.id,)
        if(user):
            sql += 'AND userId = %s'
            values +=(user.id,)
    else:
        if(user):
            sql+='userId = %s'
            values +=(user.id,)
    cursor.execute(sql,values)
    res = cursor.fetchall()
    cursor.close()
    return res

def like_user(likedUser,user):
    cursor = db.cursor(dictionary=True)
    res = get_likes(likedUser,user)
    if(not res):
        sql =   'INSERT INTO likes(likedUserId,userId) values(%s,%s)'
        cursor.execute(sql,(likedUser.id,user.id))
        db.commit()
    cursor.close()

def remove_like(likedUser,user):
    cursor = db.cursor(dictionary=True)
    res = get_likes(like_user,user)
    if(res):
        sql = 'DELETE FROM likes where likedUserId = %s and userId = %s'
        cursor.execute(sql,(likedUser.id,user.id))
        db.commit()
    cursor.close()
    
def get_user_courses(user):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT course.* FROM course 
            INNER JOIN courselist on courselist.courseId = course.courseId
            INNER JOIN user ON user.userId = courselist.userId
            WHERE user.userId = %s'''
    values = (user.id,)
    cursor.execute(sql,values)
    return cursor.fetchall()
def add_user_courses(user,courseId):
    cursor= db.cursor(dictionary=True)
    user_courses = get_user_courses(user)
    for every in user_courses:
        if(courseId==every['courseId']):
            return
    sql = 'INSERT INTO courselist(courseId,userId,isUpToDate) values(%s,%s,true)'
    cursor.execute(sql,(courseId,user.id))
    db.commit()
    cursor.close()
def change_user_course_stat(user,courseId):
    cursor = db.cursor(dictionary=True)
    user_courses = get_user_courses(user)
    for every in user_courses:
        if(courseId == every['courseId']):
            sql = 'UPDATE courselist set isUpToDate = false where courseId = %s and userId = %s'
            cursor.execute(sql,(courseId,user.id))
    db.commit()
    cursor.close()
def delete_user_course(user,courseId):
    cursor = db.cursor(dictionary=True)
    user_courses = get_user_courses(user)
    for every in user_courses:
        if(courseId == every['courseId']):
            sql = 'DELETE FROM courselist where courseId = %s and userId = %s'
            cursor.execute(sql,(courseId,user.id))
    db.commit()
    cursor.close()

def get_user_interests(user):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT interest.* FROM interest 
            INNER JOIN interestlist on interestlist.interestId = interest.interestId
            INNER JOIN user ON user.userId = interestlist.userId
            WHERE user.userId = %s'''    
    values = (user.id,)
    cursor.execute(sql,values)
    return cursor.fetchall()
def add_user_interest(user,interestId):
    print("add")
    cursor= db.cursor(dictionary=True)
    user_interests = get_user_interests(user)
    for every in user_interests:
        if(interestId==every['interestId']):
            return
    sql = 'INSERT INTO interestlist(interestId,userId) values(%s,%s)'
    cursor.execute(sql,(interestId,user.id))
    db.commit()
    cursor.close()

def delete_user_interest(user,interestId):
    cursor = db.cursor(dictionary=True)
    user_interests = get_user_interests(user)
    for every in user_courses:
        if(interestId == every['interestId']):
            sql = 'DELETE FROM interestlist where interestId = %s and userId = %s'
            cursor.execute(sql,(interestId,user.id))
    db.commit()
    cursor.close()


def get_like_count(userId):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT COUNT(likeId) as c
    FROM likes
    WHERE likedUserId = %s;'''
    cursor.execute(sql,(userId,))
    res = cursor.fetchone()
    cursor.close()
    if(res):
        return res['c']
    else:
        return 0
def check_like(likedUserId,userId):
    cursor = db.cursor(dictionary = True)
    sql = '''SELECT COUNT(likeId) as c
    FROM likes
    WHERE likedUserId = %s and userId = %s'''
    cursor.execute(sql,(likedUserId,userId))
    res = cursor.fetchone()
    cursor.close()
    
    if(res):
        if(res['c']==0):
            return False
        else:
            return True
    else:
        return False

def add_user_like(likedUserId,userId):
    cursor = db.cursor(dictionary=True)
    if(not check_like(likedUserId,userId)):
        
        sql = '''INSERT INTO likes(likedUserId,userId) values(%s,%s)'''
        cursor.execute(sql,(likedUserId,userId))
        db.commit()
    cursor.close()

def remove_user_like(likedUserId,userId):
    cursor = db.cursor(dictionary=True)
    if(check_like(likedUserId,userId)):
        sql = '''DELETE FROM likes WHERE likedUserId = %s and userId = %s'''
        cursor.execute(sql,(likedUserId,userId))
        db.commit()
    cursor.close()