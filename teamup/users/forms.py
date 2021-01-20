from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField,IntegerField,FloatField,SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from teamup.database import get_courses,get_deps, get_facs, get_unis


def dict_list_to_tuple_list(_dict):
    res = list()
    
    for every in _dict:
        key_list = list(every)
        res.append((every[key_list[0]],every[key_list[1]]))
    return res
class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    username = StringField('username',
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label=('Sign Up'))

class EditProfileForm(FlaskForm):
    
    fullName = StringField('Full Name')
    bio = TextAreaField('Bio')
    
    university = SelectField(label = 'University', coerce = int)
    faculty = SelectField(label = 'Faculty',coerce = int)
    department = SelectField(label = 'Department', coerce =int)
    yearOfStudy = IntegerField(label = 'Year of Study')
    gpa = FloatField(label = 'GPA')
    linkPhoto = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jfif','jpeg'], 'Images only')])
    linkCV = FileField('CV', validators=[FileAllowed(['pdf'], 'PDF only')])
    linkGithub = StringField('Github Link')
    submit = SubmitField(label = ('Save'))


    

