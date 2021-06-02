from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    Phone_Number=StringField('Phone Number', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    Remember_Me=BooleanField('Remember Me')
    Submit=SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    phone_number=StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 =PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_Phone_Number(self, Phone_Number):
        user=User.query.filter_by(Phone_Number=Phone_Number.data).first()
        if user is not None:
            raise ValidationError('Please use a different Phone Number.')


    