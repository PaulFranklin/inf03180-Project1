"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, AddProfile
from models import UserProfile
import os
from datetime import date, datetime
from time import strftime
from werkzeug import secure_filename
import randomfrom flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from models import UserProfile
from datetime import datetime, date
import time
from time import strftime

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/secure-page/')
@login_required
def secure_page():
    """Render a secure page on our website that only logged in users can access."""
    return render_template('secure_page.html')
    
    
    

    
@app.route ('/timeinfo/')
def timeinfo ():
    
    """  timeinfo"""
    return datetime.now().strftime('%A/%w/%b/%Y')
    
    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
   form = LoginForm()
   print('login form created')
   if request.method == 'POST':
      print('Entered Post')
      if form.validate_on_submit:  #If the form contains all required fields
         print('Form validated')
         #Create a new profile and commit it to the db.
         newprofile = UserProfile(
                                id = form.id.data,
                                first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                age=form.age.data,
                                biography=form.biography.data,
                                gender= form.gender.data,
                                username=form.username.data,
                                password=form.password.data)
         try:
            print('Trying to add new profile')
            db.session.add(newprofile)
            print('profile added')
            db.session.commit()
            print('profile commited')
            flash('profile commited to database')
            return render_template("login.html", form=form) 
         except:
            print('Exception')
            #Something went wrong when trying to add to the database.
            flash('Could not commit new contact') 
      else: #If the form does not have all fields that are required 
         print('Entered else')
         flash('All fields are required.')
   print('Return')
   return render_template('contact.html', form=form,time_info= timeinfo())

@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    form = LoginForm()
    #Fetch the first contact from db.
    profileinfo = profile.query.first()
    #if you want to fetch a specific contact you need to specify it like this,
    #contactinfo = Contact.query.filter_by(name='somenamehere').first()

    #Populate the form
    form.id.data = profileinfo.id
    form.first_name.data = profileinfo.first_name
    form.last_name.data = profileinfo.last_name
    form.age.data =profileinfo.age
    form.biography.data = profileinfo.biography
    form.gender.data = profileinfo.gender
    form.username.data = profileinfo.username
    form.password.data = profileinfo.password
    #returns the html page, along with the form        
    return render_template('profileinfo.html', form=form)
    
    
    
    
    
    
@app.route('/profile/<userid>', methods=['GET', 'POST'])
def profilesid():
    form = LoginForm()
    #Fetch the first contact from db.
    
    profileinfo = profile.query.filter_by(name='somenamehere').first()

    #Populate the form
    form.id.data = profileinfo.id
    form.first_name.data = profileinfo.first_name
    form.last_name.data = profileinfo.last_name
    form.age.data =profileinfo.age
    form.biography.data = profileinfo.biography
    form.gender.data = profileinfo.gender
    form.username.data = profileinfo.username
    form.password.data = profileinfo.password
    #returns the html page, along with the form        
    return render_template('profileinfo.html', form=form)
    
    
    
@app.route('/profiles',  methods=["GET", "POST"])
def listprofiles():
    display = db.session.query(UserProfile).all()
    if request.method=="POST":

        lists = []
        for user in display:
            
            lists.append({'Username': user.username,'id': user.id})
            display = {'Users': lists}
            
        return jsonify(display)
    return render_template('profile_lists.html',display=display)
    
    
@app.route('/profile/<int:id>', methods=["GET", "POST"])
def profileview(id):
     selected = db.session.query(UserProfile).filter_by(id=id).first()
     image_get = url_for('static', filename='images/'+selected.image)
     if request.method=="POST":
         return jsonify(id=selected.id, username = selected.username, image = selected.image, gender = selected.gender, age = selected.age, created_on = selected.created_on)
     else:
         selected_one = {'id':selected.id,'usern':selected.username,'image':image_get,'age':selected.age,'firstname':selected.firstname,'lastname':selected.lastname, 'created_on':selected.created_on,'gender':selected.gender,'biography':selected.biography}
         return render_template('profileview.html',selected_one=selected_one)
    
    
    
    
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if user is already logged in, just redirec them to our secure page
        # or some other page like a dashboard
        return redirect(url_for('secure_page'))

    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm(request.form,csrf_enabled=True)
    # Login and validate the user.
    if request.method == 'POST' and form.validate_on_submit():
        # Query our database to see if the username and password entered
        # match a user that is in the database.
        username = form.username.data
        password = form.password.data

        user = UserProfile.query.filter_by(username=username, password=password)\
        .first()

        if user is not None:
            # If the user is not blank, meaning if a user was actually found,
            # then login the user and create the user session.
            # user should be an instance of your `User` class
            login_user(user)

            flash('Logged in successfully.', 'success')
            next = request.args.get('next')
            return redirect(url_for('secure_page'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
