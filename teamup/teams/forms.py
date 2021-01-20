from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField,IntegerField,FloatField,SelectMultipleField,RadioField,DateField,widgets, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Optional
from teamup.database import get_courses,get_deps, get_facs, get_unis,get_users
from wtforms.widgets.html5 import DateTimeInput

def dict_list_to_tuple_list(_dict):
    res = list()
    
    for every in _dict:
        key_list = list(every)
        sel = ''
        if(every[key_list[1]]):
            sel += every[key_list[1]] + ' - ' 
        if(every[key_list[2]]):
            sel+= every[key_list[2]] + ' - ' 
        if(every[key_list[3]]):
            sel+=every[key_list[3]]
        res.append((every[key_list[0]],sel))
    return res


def course_code_list(_dict):
    res = list()
    i=0
    for every in _dict:
        if not (every['courseCode'] in res):
            res.append((i,every['courseCode']))
        i+=1
    return res


def util(_dict):
    res = list()
    
    for every in _dict:
        key_list = list(every)
        res.append((every[key_list[0]],every[key_list[1]]))
    return res

class CreateTeamForm(FlaskForm):
    course_choice = dict_list_to_tuple_list(get_courses())
    teamName = StringField('Team Name',validators = [DataRequired()])
    description = TextAreaField('Description',validators = [DataRequired()])
    openSpots = IntegerField('Open Spots',validators = [DataRequired()])
    isAccepting = BooleanField('Accepting',validators = [Optional()],default = 1)
    course = SelectField(label = 'Course',coerce=int, choices =course_choice)
    linkPhoto = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jfif','jpeg'], 'Images only')])
    submit = SubmitField('SUBMIT')

class ApplicationForm(FlaskForm):
    content = TextAreaField('Motivation Letter',validators=[DataRequired()])
    submit = SubmitField('SEND')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SearchteamForm(FlaskForm):
    temp = get_courses()
    course_code_choices = course_code_list(temp)
    course_code = MultiCheckboxField('Course Code',choices=course_code_choices, coerce=int)
    isAccepting = RadioField('Accepting',choices=[(0,'All'),(1,'Accepting'),(2,'Closed for Acception')],default = 0, coerce=int)
    name = StringField('Team Name')
    search = SubmitField('SEARCH')