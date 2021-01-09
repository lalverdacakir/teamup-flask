from teamup import db
from ..models import User, UserDetail
def get_user(username=None,email=None,userId=None):
    cursor = db.cursor()
    sql = 'SELECT * FROM user '
    if (username or email or userId):
        sql = sql + 'WHERE '
    if username:
        sql = sql + 'username = \'' + username + '\''
    if email:
        if 'WHERE' in sql:
            sql = sql + 'OR '
        sql = sql + 'email = \'' + email + '\' '
    if userId:
        if 'WHERE' in sql:
            sql = sql + 'OR '
        sql = sql + 'userId = \'' + str(userId) + '\' '
    print(sql)
    cursor.execute(sql)
    
    res = cursor.fetchall()
    cursor.close()
    return res
def get_user_detail(userId=None):
    cursor = db.cursor()
    sql = 'SELECT * FROM userdetail '
    if(userId):
        sql = sql + 'WHERE userId = \'' + str(userId) + '\' '
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
def insert_user(user):
    cursor = db.cursor()
    sql = 'INSERT INTO user(username,email,password) VALUES(\''+ user.username + '\',\'' + user.email + '\',\'' + user.password + '\')'
    cursor.execute(sql)
    db.commit()
    user.id= cursor.lastrowid
    sql = 'INSERT INTO userdetail(userId) VALUES(\''+ str(user.id)+ '\')'
    cursor.execute(sql)
    db.commit()
    cursor.close()


    