# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, views

import os
import functools
import urllib,urllib2
import json
from datetime import datetime, timedelta

#configuration
SECRET_KEY = '\x95\x89d\xc6&\r@\xdd\xcb\x08\xac\xab\xe4\xf6\x9e\x00\x1d]\x9fR\x16\xa3\xa5Q'

comicninja = Flask(__name__)
comicninja.config.from_object(__name__)

####### SEND THIS TO ITS OWN FILE, EVENTUALLY ########
# Convenience methods
def login_required(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        if "username" in session:
            return f(*args,**kwargs)
        else:
            flash("Enter the Dōjō with your secret Comic Ninja name and password.")
            return redirect(url_for("home"))
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

# The comicninja Object Classification
class Home(views.MethodView):
    def get(self):
        context = {}
        context["page_title"] = "Welcome to the Comic Ninja Dōjō"
        return render_template("home.html5")
    @login_required
    def post(self):
        pass

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
# Rules for the comicninja urls, so the comicninjas get to where thy want to go
comicninja.add_url_rule("/",
    view_func = Home.as_view('home'),
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
    port = 5000
    comicninja.debug = True
    comicninja.run(host="0.0.0.0",port=port)
