from . import db
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

class UserProfile(db.Model):
    
    __tablename__ = "Profiles"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String,nullable=False)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    biography = db.Column(db.Text,nullable=False)
    
    
    
    def __init__(self,first_name,last_name, age,username,password, biography,gender,id):
        self.first_name = first_name
        self.last_name = last_name
        self.age= age
        self.biography = biography
        self.gender= gender
        self.username = username
        self.password =password
        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
