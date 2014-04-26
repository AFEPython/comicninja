from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, views
from pymongo import MongoClient
from ConfigParser import SafeConfigParser
from datetime import datetime, timedelta

import os
import os.path
import shutil
import functools
import urllib,urllib2
import json

#configuration
SECRET_KEY = '\x95\x89d\xc6&\r@\xdd\xcb\x08\xac\xab\xe4\xf6\x9e\x00\x1d]\x9fR\x16\xa3\xa5Q'

comicninja = Flask(__name__)
comicninja.config.from_object(__name__)

mongo_client = MongoClient()
db = mongo_client['comic_ninja_database']
users = db['users']

####### SEND THIS TO ITS OWN FILE, EVENTUALLY ########
# Convenience methods
def login_required(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        if "username" in session:
            return f(*args,**kwargs)
        else:
            flash("Enter the Dojo with your secret Comic Ninja name and password.")
            return redirect(url_for("login"))
    return wrapper;

def handle_logout(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        if "logout" in request.form:
            session.pop("username",None)
            return redirect(url_for("home"))
        else:
            return f(*args,**kwargs)
    return wrapper

def salty_password(username, password):
    '''@returns a salted password given a username and plain text pw.'''
    user_hashbrown = SHA256.new(username).hexdigest()
    salt = ''.join(
       [user_hashbrown[i] for i in range(0, len(user_hashbrown), 3)]
    )
    password_hash = SHA256.new(salt+password).hexdigest()
    return password_hash

# The comicninja Object Classification
class Home(views.MethodView):
    def get(self):
        context = {}
        context["page_title"] = "Welcome to the Comic Ninja Dojo"
        return render_template("home.html5")

class Login(views.MethodView):
    def get(self):
        # Return a login page.
        context = {}
        context["page_title"] = "Enter the Comic Ninja Dojo"
        return render_template("login.html5")
    def post(self):
        # Process the login request.
        u = request.form['username']
        p = request.form['password']
        salted_pass = salty_password(u, p)
	
	user = users.find_one({'username': u, 'password': p})
	if user is not None:
           print "You're IN!"
        return 'Almost implemented.'

class Register(views.MethodView):
    def get(self):
        # Return a register page.
        context = {}
        context["page_title"] = "Join the Comic Ninja Dojo"
        return render_template("register.html5", **context)

    def post(self):
        context = {}
        context["page_title"] = "Join the Comic Ninja Dojo"
        errors = []
        # Process the registration request.
        if request.form['username']:
            if request.form['password'] == request.form['password1']:
                self.register(request.form)
            else:
                errors.append('On the job, incorrectly typed passcodes may hamper your unit\'s security. Please be more careful in the future. You may attempt registration again.')
        else:
            errors.append('Please choose a Ninja Codename so that we may know how to address you.')
        context['errors'] = errors

        return render_template("register.html5", **context)

    def register(self, form):
        print "You are registered as {0}, {1}".format(form['username'], form['name'])
        new_user = {
            'username': form['username'],
            'name': form['name'],
            'email': form['email'],
            'password': salty_password(form['username'], form['password'])
        }
        new_user_id = users.insert(new_user)


class ComicList(views.MethodView):
    @login_required
    def get(self):
        pass
    @login_required
    def post(self):
        pass

class ComicEdit(views.MethodView):
    @login_required
    def get(self):
        pass
    @login_required
    def post(self):
        pass

class ComicDelete(views.MethodView):
    @login_required
    def delete(self):
        pass

##### SEND THIS CODE TO ITS OWN FILE, EVENTUALLY #####
# Rules for the comicninja urls, so the comicninjas get to where they want to go
comicninja.add_url_rule("/",
    view_func = Home.as_view('home'),
    methods = ["GET"])

comicninja.add_url_rule("/login",
    view_func = Login.as_view('login'),
    methods = ["GET","POST"])

comicninja.add_url_rule("/register",
    view_func = Register.as_view('register'),
    methods = ["GET","POST"])

comicninja.add_url_rule("/comics/list",
    view_func = ComicList.as_view("comic_list"),
    methods = ["GET","POST"])

comicninja.add_url_rule("/comics/<comic_id>/edit",
    view_func = ComicEdit.as_view("edit_comic"),
    methods = ["GET","POST"])

comicninja.add_url_rule("/comics/<comic_id>/delete",
    view_func = ComicDelete.as_view("delete_comic"),
    methods = ["DELETE"])

if (__name__ == "__main__"):
    config = SafeConfigParser()
    config_name = os.path.join(comicninja.root_path, '..', 'comicninja.cfg')
    if not os.path.isfile(config_name):
        shutil.copyfile(os.path.join(comicninja.root_path, '..', 'comicninja.default.cfg'), config_name)
    config.read(config_name)

    port = config.getint('server', 'port')
    comicninja.debug = config.getboolean('server', 'debug')
    comicninja.run(host="0.0.0.0",port=port)

