import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from models import Resource, Task


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pmappdb.db'

db = SQLAlchemy(app)

from pmapp import routes

#need to import the routes here otherwise we'll create a circular import if we have this line above app=Flask(__name__)