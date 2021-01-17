from teamup import db
from .models import User
def get_users():
    cursor = db.cursor(dictionary = True)
    sql = 'SELECT userId, username FROM user'
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
def get_unis():
    cursor = db.cursor(dictionary=True)
    sql = 'SELECT * FROM university'
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
def add_uni(name):
    cursor = db.cursor(dictionary=True)
    name = name.upper()
    sql = 'INSERT INTO university(uniName) values(%s)'
    
    cursor.execute(sql,(name,))
    
    db.commit()
    cursor.close()

def get_deps():
    cursor = db.cursor(dictionary=True)
    
    
    sql = 'SELECT * FROM department'
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
def add_dep(name):
    cursor = db.cursor(dictionary=True)
    name = name.upper()
    
    sql = 'INSERT INTO department(depName) values(%s)'
    
    cursor.execute(sql,(name,))
    
    db.commit()
    cursor.close()

def get_facs():
    cursor = db.cursor(dictionary=True)
    sql = 'SELECT * FROM faculty'
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
def add_fac(name):
    
    cursor = db.cursor(dictionary=True)
    name = name.upper()
    sql = 'INSERT INTO faculty(facName) values(%s)'
    
    cursor.execute(sql,(name,))
    
   
    db.commit()
    cursor.close()



def get_courses():
    cursor = db.cursor(dictionary=True)
    sql = 'SELECT * FROM course'
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
def add_course(course_dict):
    cursor = db.cursor(dictionary=True)
    sql = 'INSERT INTO course(courseName,courseCode,courseCRN) values(%s,%s,%s)'
    
    values = (course_dict['courseName'],course_dict['courseCode'],course_dict['courseCRN'])
    cursor.execute(sql,values)
    db.commit()
    cursor.close()
