from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField,TextField,DateField,IntegerField,SelectField,TextAreaField
from wtforms.validators import InputRequired,required

class LoginForm(FlaskForm):
    first_name = TextField('First Name',validators=[required()])
    last_name = TextField('First Name',validators=[required()])
    age = IntegerField('Age',validators=[required()])
    gender = SelectField('Gender',validators=[required()],choices=[('Male','1'),('Female','2'),('3','3'),('4','4'),('5','5')])
    biography = TextAreaField('Biography',validators=[required()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField("Submit")