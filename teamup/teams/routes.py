from flask import render_template, url_for, flash, redirect, request, Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
from teamup import db
from .forms import CreateTeamForm,ApplicationForm,SearchteamForm
from teamup.users.database import get_user,get_user_detail
from teamup.teams.database import get_teams,get_total_open_spots,get_accepting_team_count,create_team,delete_team_info,update_team_data,get_team,get_user_apps,get_user_teams,update_user_app,add_user_app,get_team_members,get_team_applications,get_app,add_user_team,accept_user_team,deny_user_team,delete_user_app
from teamup.teams.utils import filter_by_name,filter_by_isAccepting,filter_by_course
teams = Blueprint('teams',__name__)
@teams.route('/main',methods=['GET','POST'])
@login_required
def main():
    teams = get_teams() #dictionary
    form = SearchteamForm()
    accepting = get_accepting_team_count()
    open_spots = get_total_open_spots()
    if form.validate_on_submit():
        
        if(form.course_code.data != []):
            print("course: ",form.course_code.data)

            
            teams = filter_by_course(form.course_code.data,form.course_code_choices,teams)
        
      
        if(form.isAccepting.data != 0):
            print("isAccepting: ",form.isAccepting.data)
            
            teams = filter_by_isAccepting(form.isAccepting.data,teams)
        if(form.name.data != ""):
            print("name: ",form.name.data)
            
            teams = filter_by_name(form.name.data,teams)
    parameters = {
        "usr": current_user,
        "teams": teams,
        "accepting": accepting,
        "open_spots": open_spots
    }
    return render_template('ads.html',form=form,parameters=parameters)

@teams.route('/view_team/<int:teamId>',methods = ['GET'])
def view_team(teamId):
    team = get_team(teamId = teamId)

    if(team):
        members = get_team_members(team['teamId'])
        if(members):
            members_with_details = list()
            print(members)
        else:
            members_with_details = None
        for member in members:
            temp = get_user_detail(member['userId'])
            members_with_details.append(temp)
        admin = get_user(userId = team['adminUserId'])
        if(admin):
            admin = admin[0]
            admin = get_user_detail(admin['userId'])
        applications = get_team_applications(teamId)
         
        par={
        "usr": current_user,
        "team": team,
        "members": members_with_details,
        "admin": admin,
        "applications": applications
        }
        print(par)
        return render_template('team_detail.html',parameters = par)
    else:
        return redirect(url_for('main.home'))

@teams.route('/create_team',methods=['GET','POST'])
@login_required
def createTeam():
    form = CreateTeamForm()
    if form.validate_on_submit():
        last_row = create_team(current_user,form)
        return redirect(url_for('teams.view_team',teamId = last_row))
    parameters = {
        "usr": current_user,
        "action": url_for('teams.createTeam'),
        "photo": "img/team_img/dummy.jpeg"
    }
    return render_template('create_team.html',form = form,parameters=parameters)
@teams.route('/update_team/<int:teamId>',methods=['GET','POST'])
@login_required
def update_team(teamId):
    team = get_team(teamId)
    if(team):
        if(team['adminUserId']==current_user.id):

            form = CreateTeamForm()
            if form.validate_on_submit():
                
                try:
                    update_team_data(teamId,form)
                    flash('Updated the team information succesfully','success')
                except:
                    flash('Failed to update team data','danger')
                return redirect(url_for('teams.view_team',teamId = teamId))

            form.teamName.default = team['teamName']
            form.description.default = team['description']
            form.openSpots.default = team['openSpots']
            form.course.default = team['courseId']
            form.isAccepting.default = team['isAccepting']
            form.process()
        else:
            return redirect(url_for('teams.createTeam')) 
    else:
        return redirect(url_for('teams.createTeam'))    
    parameters = {
        "usr": current_user,
        "action": url_for('teams.update_team',teamId = teamId),
        "photo": team['linkPhoto']
    }

        
    return render_template('create_team.html',form = form,parameters=parameters)

@teams.route('/delete_team/<int:teamId>',methods=['POST'])
@login_required
def delete_team(teamId):
    team = get_team(teamId)
    if(team):
        if(team['adminUserId']==current_user.id):
            try:
                delete_team_info(teamId)
                flash('Deleted team','success')
            except:
                flash('Failed to delete the team','danger')
            
            return redirect(url_for('main.home'))
        else:
            flash('Access denied','danger')
    else:
        flash('That team is not exists or already deleted','danger')
    return redirect(url_for('main.home'))

@teams.route('/apply/<int:teamId>',methods = ['GET','POST'])
@login_required
def apply(teamId):
    team = get_team(teamId)
    
    if(team):
        
        if(team['isAccepting']):
            
            form = ApplicationForm()
            already_applied = False
            if(team['adminUserId']==current_user.id):
                
                flash('admin','danger')
                return redirect(url_for('teams.view_team',teamId = teamId))
            
            applications = get_user_apps(current_user.id)
            
            for every in applications:
                
                if(every['teamId']==teamId):
                    
                    #user alreday applied
                    if(every['status']=='In Process'):
                        form.content.default = every['content']
                        form.process()
                        already_applied = True
                        break
                    
                        
            teams = get_user_teams(current_user.id)
            
            for every in teams:
                if(every['teamId']==teamId):
                    flash('You are already a member of this team','success')
                    return redirect(url_for('teams.view_team',teamId = teamId))

            
            if(form.validate_on_submit()):
                if(already_applied):
                    try:
                        update_user_app(current_user,teamId,form)
                        flash('Updated your application','success')
                    except:
                        flash('Failed to update the application. Please try again.','danger')
                 
                    
                else:
                    try:
                        add_user_app(current_user,teamId,form)
                        flash('Saved your application','success')
                    except:
                        flash('Failed to save you application','danger')
                   
               
                return redirect(url_for('teams.view_team',teamId = teamId))

            parameters = {
                "usr":current_user,
                "team":team
            }
            return render_template('application.html',parameters = parameters,form=form)
        else:
            flash('isAcc','danger')
            return redirect(url_for('teams.view_team',teamId = teamId))
    else:
        lash('isAcc','danger')
        return redirect(url_for('main.home'))
        
@teams.route('/accept_application/<int:appId>',methods=['POST'])
@login_required
def accept_application(appId):
    
    application = get_app(appId)
   
    if(application):
        if current_user.id == application['adminUserId']:
            
            try:
                add_user_team(application['teamId'],application['userId'])
                flash('Added the user to the team','success')
                try:
                    accept_user_team(application['teamId'],application['userId'])
                    flash('Accepted the application','success')
                except:
                    flash('Failed to accept application','danger')
            except:
                flash('Failed to add user to team','danger')
            return redirect(url_for('teams.view_team',teamId = application['teamId']))
        else:
            flash('Permission denied','danger')
            return redirect(url_for('teams.view_team',teamId = application['teamId']))
    else:
        flash('Failed. Try again.','danger')
    return redirect(url_for('teams.view_team',teamId = application['teamId']))

@teams.route('/deny_application/<int:appId>',methods=['POST'])
@login_required
def deny_application(appId):
    
    application = get_app(appId)
    if(application):
        if current_user.id == application['adminUserId']:
            try:
                deny_user_team(application['teamId'],application['userId'])
                flash('Denied the application','success')
            except:
                flash('Failed to deny application','danger')
            return redirect(url_for('teams.view_team',teamId = application['teamId']))
        else:
            flash('Permission denied','danger')
            return redirect(url_for('teams.view_team',teamId = application['teamId']))
    else:
        flash('Failed. Try again.','danger')
    return redirect(url_for('teams.view_team',teamId = application['teamId']))

@teams.route('/delete_application/<int:appId>',methods=['POST'])
@login_required
def delete_application(appId):
    application = get_application(appId)
    if(application):
        try:
            delete_user_app(appId)
            flash('Deleted the application','success')
        except:
            flash('Failed to delete the application','danger')
        
    else:
        flash('Application doesn\'t exists.')
    redirect(url_for('teams.my_applications'))

@teams.route('/my_applications',methods=['GET'])
@login_required
def my_applications():
    applications = get_user_apps(current_user.id)
    parameters={
        "usr": current_user,
        "applications": applications
    }

    return render_template('my_applications.html',parameters = parameters)


