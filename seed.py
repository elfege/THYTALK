"""Seed file to make sample data for pets db."""

from models import User, Post, Tag, PostTag, Like, Response, bcrypt, db
from app import app
# from random import *



from datetime import datetime

# with app.app_context():
#     connect_db(app)

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

#hashed "password":
hashed = bcrypt.generate_password_hash("password")
# turn bytes string into normal (unicode utf8) string
hashed_utf8 = hashed.decode("utf8")

# Add Users
Elfege = User(name='Elfege', 
              last_name="Leylavergne",
              username='elfege',
              password=hashed_utf8,
              img_url="https://elfege.com/images/elfege.jpg")
Paul = User(name='Bob', 
            last_name="Marley",
            username='bob',
            password=hashed_utf8,
            img_url="https://elfege.com/images/bobmarley.jpg")
Jack = User(name='Jack', 
            last_name="Camstone",
            username='jack',
            password=hashed_utf8) # no url, test default value

# Add new objects to session, so they'll persist
db.session.add(Elfege)
db.session.add(Paul)
db.session.add(Jack)

# create a longer list of users for tests purposes
# for a in map(chr, range(97, 123)):
#     a = User(name=a, 
#                 last_name="Camstone",
#                 username= "user_"+a,
#                 password=hashed_utf8) # no url, test default value
#     db.session.add(a)


# Elfege = User(name='Elfege', last_name="Leylavergne", img_url="https://elfege.com/images/elfege.jpg", post="test test")



# Commit to users db
db.session.commit()

# create a first post
usr = User.query.filter_by(name="Elfege").first()

# post_code = usr.name + str(randint(1, 10000000000))

post = Post(
    user_id=usr.id,
    post_author=usr.full_name,
    post_title="Welcome",
    post="Welcome to THY TALK! The site where free speech is for real!" 
)
post2 = Post(
    user_id=usr.id,
    post_author=usr.full_name,
    post_title="Welcome",
    post="Here you can speak freely to whoever you may come across. With no selective algorithm, you will meet people just like you do in real life: randomly! Not just people who think like you, eat like you or listen to the same music as you.",
    # pub_date=datetime.datetime.now
)

# see: https://mike.depalatis.net/blog/sqlalchemy-timestamps.html

db.session.add(post)
db.session.add(post2)
db.session.commit()

# assign a tag to a post 

tag_to_first_post = Tag(
    post_id = post.id,
    tag = "first test tag"    
)
tag_to_first_post_2 = Tag(
    post_id = post.id,
    tag = "second test tag"    
)

tag_to_second_post = Tag(
    post_id = post2.id,
    tag = "first test tag 2"    
)
tag_to_second_post_2 = Tag(
    post_id = post2.id,
    tag = "second test tag 2"    
)

db.session.add(tag_to_first_post)
db.session.add(tag_to_first_post_2)
db.session.add(tag_to_second_post)
db.session.add(tag_to_second_post_2)

db.session.commit()

response_1_to_1st_post = Response(
    user_id=usr.id,
    post_id=post.id,
    reply_author="Elfege",
    response = "You can reply to any post. However, you can't (yet) reply to replies in infinite cascades! This isn't ready-it (yet!) :) "    
)
response_2_to_1st_post = Response(
    user_id=usr.id,
    post_id=post.id,
    reply_author="Elfege",
    response = "Be ready for when one can create their own threads!"    
)

db.session.add(response_1_to_1st_post)
db.session.add(response_2_to_1st_post)

db.session.commit()

# create a like for user 1, post 1
like_post1 = Like(user_id=usr.id, post_id=post.id)
like_post2 = Like(user_id=usr.id, post_id=post2.id)

db.session.add(like_post1)
db.session.add(like_post2)
db.session.commit()


