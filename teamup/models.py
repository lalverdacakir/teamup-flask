from flask import current_app
from teamup import login_manager, db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    db.reconnect()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user where userId = %s',(user_id,))
    res = cursor.fetchone()
    cursor.close()
    return User(res)



class User(UserMixin):


    def __init__(self,_dict):

        if('userId' in _dict):
            self.id = _dict['userId']
        self.email =_dict['email']
        self.username = _dict['username']
        self.password = _dict['password']
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"


