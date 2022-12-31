from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional
from wtforms.widgets import TextArea
from flask_wtf.recaptcha import RecaptchaField
import os

try:
    from keys import RECAPTCHA_PRIVATE_KEY_keys, RECAPTCHA_PUBLIC_KEY_keys
except:
    RECAPTCHA_PRIVATE_KEY_keys="nokey"
    RECAPTCHA_PUBLIC_KEY_keys="nokey"
    
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", RECAPTCHA_PUBLIC_KEY_keys)
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", RECAPTCHA_PRIVATE_KEY_keys)


class AddUser(FlaskForm):
    """form that adds a new user"""

    name = StringField("First Name",
                       validators=[InputRequired()],
                       )

    last_name = StringField("Last Name",
                            validators=[InputRequired()],
                            )

    username = StringField("User Name",
                            validators=[InputRequired()],
                            )
    
    password = PasswordField("Password",
                           validators=[InputRequired()])

    img_url = StringField("Photo url",
                          validators=[Optional(), URL()],
                          )
    recaptcha = RecaptchaField()

class LoginForm(FlaskForm):
    username = StringField("User Name", 
                           validators=[InputRequired()],
                       )
    password = PasswordField("Password",
                           validators=[InputRequired()])

class AddComment(FlaskForm):
    """form that adds a new comment on a user's page"""

    post_title = StringField("Title",
                             validators=[
                                 InputRequired(), Length(min=5, max=30)]
                             )
    post_content = TextAreaField("Comment",
                               validators=[InputRequired(), Length(
                                   min=5, max=30000)],
                               widget=TextArea()
                            )
    recaptcha = RecaptchaField()

class AddResponse(FlaskForm):
    """form that add a response to a post"""
    response = StringField('Response',
                           validators=[InputRequired()],
                           widget=TextArea()
                           )
    recaptcha = RecaptchaField()

class UpdateUser(FlaskForm): #TODO : extend User class?
    """form to edit a user"""

    name = StringField("First Name",
                       validators=[InputRequired()],
                       render_kw={'readonly': True}
                       )
    last_name = StringField("Last Name",
                            validators=[InputRequired()],
                            render_kw={'readonly': True}
                            )
    username = StringField("User Name",
                            validators=[InputRequired()],
                            render_kw={'readonly': True}
                            )
    old_password = PasswordField("Old Password",
                           validators=[InputRequired()]
                           )    
    new_password = PasswordField("New Password",
                           validators=[InputRequired()]
                           )
    img_url = StringField("Photo url",
                          validators=[Optional(), URL()],
                          )
    recaptcha = RecaptchaField()
    
    submit = SubmitField()