from teamup import db,app
from ..models import User
from datetime import date
import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(form_picture.filename)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/team_img', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def create_team(user,form):
    
    cursor = db.cursor(dictionary=True)
    sql = 'INSERT INTO team(adminUserId,teamName,courseId,description,openSpots,createDate,isAccepting,linkPhoto) values(%s,%s,%s,%s,%s,%s,%s,%s)'
    path = ''
    if(form.linkPhoto.data):
        path = 'img/team_img/' + save_picture(form.linkPhoto.data)
    else:
        path = 'img/team_img/dummy.jpeg'
        
    
    values = (user.id,form.teamName.data,form.course.data,form.description.data,form.openSpots.data,date.today(),form.isAccepting.data,path)
    cursor.execute(sql,values)
    db.commit()
    res = cursor.lastrowid
    cursor.close()
    return res

def get_team(teamId):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT team.*,course.*,user.username FROM team 
        LEFT JOIN user ON user.userId = team.adminUserId
        LEFT JOIN course on course.courseId = team.courseId
        WHERE team.teamId = %s
    '''
    cursor.execute(sql,(teamId,))
    res = cursor.fetchone()
    cursor.close()
    return res

def get_user_apps(userId):
    cursor = db.cursor(dictionary=True)
    sql = ''' SELECT user.*,team.*,application.* FROM application 
            INNER JOIN user ON user.userId = application.userId
            INNER JOIN team on team.teamId = application.teamId
            WHERE user.userId = %s'''
    values = (userId,)
    cursor.execute(sql,values)
    return cursor.fetchall()
def add_user_app(user,teamId,form):
    cursor= db.cursor(dictionary=True)
    user_apps = get_user_apps(user.id)
    for every in user_apps:
        if(teamId==every['teamId']):
            return 
    sql = 'INSERT INTO application(teamId,userId,content,applyDate,modified,status) values(%s,%s,%s,%s,%s,%s)'

    values = (teamId,user.id,form.content.data,date.today(),date.today(),'In Process')
 
    cursor.execute(sql,values)
    db.commit()
    cursor.close()

def update_user_app(user,teamId,form):
    cursor= db.cursor(dictionary=True)
    user_apps = get_user_apps(user.id)
    for every in user_apps:
        if(teamId==every['teamId']):
            sql = 'UPDATE application set content = %s, modified = %s where teamId = %s and userId = %s'
            cursor.execute(sql,(form.content.data,date.today(), teamId,user.id))
            db.commit()
            cursor.close()
            return
    cursor.close()
    return

def change_status_app(appliedUserId,teamId):
    cursor= db.cursor(dictionary=True)

    user_apps = get_user_apps(appliedUserId)
    for every in user_apps:
        if(teamId==every['teamId']):
            sql = 'UPDATE application set content = %s, modified = %s where teamId = %s and userId = %s'
            cursor.execute(sql,(every['content'],date.today(), teamId,appliedUserId))
            db.commit()
            cursor.close()
            return
    cursor.close()
    return

def delete_user_app(appId):
    cursor = db.cursor(dictionary=True)
    sql = 'DELETE FROM application where applicationId = %s'
    cursor.execute(sql,(appId,))
    db.commit()
    cursor.close()

def get_user_teams(userId):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT team.*,course.* FROM teamlist 
        INNER JOIN user ON user.userId = teamlist.userId
        INNER JOIN  team on team.teamId = teamlist.teamId
        LEFT JOIN course on course.courseId = team.courseId
        WHERE user.userId = %s ORDER BY isAccepting desc
    '''
    values = (userId,)
    cursor.execute(sql,values)
    return cursor.fetchall()
def get_admin_teams(userId):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT team.*,course.* FROM team 
        LEFT JOIN course on course.courseId = team.courseId
        WHERE team.adminUserId = %s ORDER BY isAccepting desc
    '''
    values = (userId,)
    cursor.execute(sql,values)
    return cursor.fetchall()

def set_is_accepting(teamId,value):
    cursor = db.cursor(dictionary=True)
 
    sql = 'UPDATE team SET isAccepting = %s WHERE teamId = %s'
   
    values = (value,teamId)
    cursor.execute(sql,values)
    db.commit()
    cursor.close()
    

def delete_team_info(teamId):
    cursor= db.cursor(dictionary=True)
    team = get_team(teamId)
    if(team):
        sql = 'DELETE FROM team WHERE teamId = %s'
        cursor.execute(sql,(teamId,))
        db.commit()
        cursor.close()


def add_user_team(teamId,userId):
    cursor = db.cursor(dictionary=True)
    sql = 'INSERT INTO teamlist(teamId,userId) values(%s,%s)'
    cursor.execute(sql,(teamId,userId))
    db.commit()
    cursor.close()
def change_open_spots(number,teamId):
    cursor = db.cursor(dictionary=True)
    sql = 'SELECT openSpots FROM team where teamId = %s'
    cursor.execute(sql,(teamId,))
    res = cursor.fetchone()
    spots = 0
    if(res):
        spots = res['openSpots']
        spots += number
        sql='UPDATE team SET openSpots = %s WHERE teamId = %s'
        cursor.execute(sql,(spots,teamId))
        if(spots<=0):
            set_is_accepting(teamId,False)
            
        
        db.commit()
    cursor.close()
    
def accept_user_team(teamId,userId):
    cursor = db.cursor(dictionary=True)
    sql = 'UPDATE application SET status=%s WHERE teamId = %s and userId = %s'
    cursor.execute(sql,('Accepted',teamId,userId))
    db.commit()
    change_open_spots(-1,teamId)
    cursor.close()

def deny_user_team(teamId,userId):
    cursor = db.cursor(dictionary=True)
    sql = 'UPDATE application SET status=%s WHERE teamId = %s and userId = %s'
    cursor.execute(sql,('Denied',teamId,userId))
    db.commit()
    cursor.close()
def remove_user_team(teamId,userID):
    cursor = db.cursor(dictionary = True)
    sql = 'DELETE FROM teamlist where teamId = %s and userId = %s'
    cursor.execute(sql,(teamId,userID))

def get_team_members(teamId):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT user.* FROM teamlist 
        INNER JOIN  user on user.userId = teamlist.userId
        WHERE teamlist.teamId = %s
    '''
    values = (teamId,)
    cursor.execute(sql,values)
    res = cursor.fetchall()
    cursor.close()
    return res

def get_team_applications(teamId):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT user.*,userdetail.fullName,userdetail.linkPhoto,application.* FROM application 
        INNER JOIN  user on user.userId = application.userId
        INNER JOIN userdetail on userdetail.userId = application.userId
        WHERE application.teamId = %s
    '''
    values = (teamId,)
    cursor.execute(sql,values)
    res = cursor.fetchall()
    cursor.close()
    return res

def get_app(appId):
    cursor = db.cursor(dictionary=True)
    sql = '''SELECT user.*,userdetail.fullName,userdetail.linkPhoto,application.*,team.* FROM application 
        INNER JOIN  user on user.userId = application.userId
        INNER JOIN team on team.teamId = application.teamId
        INNER JOIN userdetail on userdetail.userId = application.userId
        WHERE application.applicationId = %s
    '''
    values = (appId,)
    cursor.execute(sql,values)
    res = cursor.fetchone()
    cursor.close()
    return res


def update_team_data(teamId,form):
    cursor = db.cursor(dictionary=True)
    team = get_team(teamId = teamId)
    sql = '''UPDATE team 
            SET teamName = %s, courseId = %s, description = %s, openSpots = %s, isAccepting = %s, linkPhoto = %s
            WHERE teamId = %s'''
    path = ''
    if(form.linkPhoto.data):
        path = 'img/team_img/' + save_picture(form.linkPhoto.data)
    else:
        path = team['linkPhoto']
        
    
    values = (form.teamName.data,form.course.data,form.description.data,form.openSpots.data,form.isAccepting.data,path,teamId)
   
    cursor.execute(sql,values)
    db.commit()
    cursor.close()
def get_accepting_team_count():
    cursor = db.cursor(dictionary=True)
    sql='''select team.isAccepting, count(*) as count from team
        group by team.isAccepting'''   
    cursor.execute(sql)
    res = cursor.fetchall()
    for each in res:
        if each['isAccepting']==1:
            return each['count']
    cursor.close()
    return 0
def get_course_team_count():
    cursor = db.cursor(dictionary = True)
    sql = '''
            SELECT course.courseName, count(team.courseId) as c FROM team
            INNER JOIN course ON course.courseId = team.courseId
            GROUP BY team.courseId
    '''
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
def get_total_open_spots():
    cursor = db.cursor(dictionary=True)
    sql='''select sum(openSpots) as sum from team where team.isAccepting = 1'''   
    cursor.execute(sql)
    res = cursor.fetchone()
   
    cursor.close()
    return res['sum']


def get_teams():
    cursor = db.cursor(dictionary = True)
    sql = '''SELECT team.*,course.* FROM team 
            LEFT JOIN course on course.courseId = team.courseId ORDER BY isAccepting desc, openSpots desc
            '''
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    return res
"""def filterTeam(courseIdList = None,isAccepting = None, name = None,date=None):
    sql='''SELECT course.*,team.*,teamlist.*,userdetail.*"""
