"""Seed file to make sample data for talk db."""

from models import User, Post, Tag, PostTag, Like, Response, bcrypt, db
from app import app
# from random import *



from datetime import datetime

# with app.app_context():
#     connect_db(app)

# Create all tables
db.drop_all()
db.create_all()
