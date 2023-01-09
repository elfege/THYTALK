"""Demo file showing off a model for SQLAlchemy."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
from flask import flash

db = SQLAlchemy()

bcrypt = Bcrypt()

DEFAULT_URL = "\static\logo.jpg"


def connect_db(app):
    """Connect this database to provided Flask app.

    called by the Flask app.
    """
    with app.app_context():
        db.app = app
        db.init_app(app)


class Like(db.Model):
    """store upvotes mapping user id and post id"""

    __tablename__ = "likes"

    # id = db.Column(db.Integer,
    #                autoincrement=True,
    #                unique=True
    #                )
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True
                        )
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)


class Like_reply(db.Model):
    """store upvotes"""

    __tablename__ = "likes_reply"

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True
                        )

    reply_id = db.Column(db.Integer,
                         db.ForeignKey('responses.id'),
                         primary_key=True)


class SavedArticle(db.Model):
    """store articles saved by users"""

    __tablename__ = "savedarticles"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))

    title = db.Column(db.String(500))

    url = db.Column(db.String(50000))

class LikedArticle(db.Model):
    """store liked articles"""

    __tablename__ = "liked_articles"
    
    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id")
                        )

    title = db.Column(db.Text)
    
    url = db.Column(db.Text)

class User(db.Model):
    """Create a list of users with attributes"""

    __tablename__ = "users"

    __table_args__ = (
        db.UniqueConstraint('name', 'last_name',
                            name='unique_name_and_last_name'),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    last_name = db.Column(
        db.String(50),
        nullable=True
    )
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.Text,
        nullable=False
    )
    img_url = db.Column(
        db.String(5000),
        nullable=True,
        default=DEFAULT_URL
    )
    
    is_online = db.Column(
        db.Boolean, 
        default=False,
        nullable=False     
    )

    #post = db.relationship("Post")

    posts = db.relationship("Post",
                            backref="user")

    responses = db.relationship("Response",
                                backref="user")

    liked_posts = db.relationship('User',
                                  secondary="likes",
                                  primaryjoin=(Like.user_id == id)
                                  )
 
    liked_replies = db.relationship('User',
                                    secondary="likes_reply",
                                    primaryjoin=(Like_reply.user_id == id)
                                    )
    
    saved_articles = db.relationship('User',
                                     secondary="savedarticles",
                                     primaryjoin=(SavedArticle.user_id == id)
                                     )

    liked_articles = db.relationship('User',
                                     secondary="liked_articles",
                                     primaryjoin=(LikedArticle.user_id == id)
                                     )
    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.name} {self.last_name}"

    def greet(self):
        """Greet using name."""

        return f"I'm {self.name} the {self.species or 'thing'}"

    def update_online_status(self, B):
        self.is_online = B
        db.session.merge(self)
        db.session.commit()
    
    def update_user(self, name, last_name, img_url, new_password, old_password, username):
        """Update/edit user info"""

        if (self.authenticate(self.username, old_password)):
            self.name = name
            self.last_name = last_name
            self.image_url = img_url
            self.posts = self.posts
            self.responses = self.responses
            self.liked_posts = self.liked_posts
            self.liked_replies = self.liked_replies
            self.saved_articles = self.saved_articles

            hashed_pwd = bcrypt.generate_password_hash(
                new_password).decode('UTF-8')

            self.password = hashed_pwd
            
            print(f"////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
            print(f" self => {self}")
            print(f"self.password = {self.password}")
            
            db.session.merge(self)
            db.session.commit()

    @classmethod
    def register(cls, name, last_name, img_url, username, password):
        """REgister user w/hashed password & return user"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            name=name,
            last_name=last_name,
            username=username,
            password=hashed_pwd,
            img_url=img_url
        )

        db.session.add(user)
        db.session.commit()
        # return user

    @classmethod
    def authenticate(cls, username, password):
        """"Validate that user exists and password is correct.

        Return user if valid, else return False"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

    def __repr__(self):
        """Show info about user."""
        return f"<User {self.id} {self.name} {self.last_name} {self.img_url}>"


class Post(db.Model):
    """Posts db"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    post_author = db.Column(
        db.Text,
        nullable=False,
        unique=False
    )

    post_title = db.Column(
        db.Text(),
        nullable=False,
    )

    post = db.Column(
        db.String(50000),
        nullable=False

    )

    pub_date = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )
    
    article_title = db.Column(
        db.Text(),
        nullable=True
    )
    article_url = db.Column(
        db.Text(),
        nullable=True
    )
    article_imgurl = db.Column(
        db.Text(),
        nullable=True
    )
    article_description = db.Column(
        db.Text(),
        nullable=True
    )
    

    tags = db.relationship('Tag',
                           backref='posts')

    tags = db.relationship('PostTag',
                           backref='posts')

    responses = db.relationship('Response',
                                backref='post')

    likes = db.relationship(
        "Post",
        secondary="likes",
        primaryjoin=(Like.post_id == id),
    )
   

    def __repr__(self):
        """Show info about user's posts."""

        return f"<Post {self.post_author} {self.post}>"

    @classmethod
    def get_posts_by_id(cls, id):
        """Get all posts matching a user's id"""

        return cls.query.filter_by(user_id=id).all()


class PostTag(db.Model):
    """Intermediate table that joins Post and Tag tables"""

    ___tablename__ = "postTags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)


class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id')
    )

    tag = db.Column(db.String(20),
                    nullable=False)

    # direct navigation: tag -> post & back
    posts = db.relationship('Post',
                            #    secondary="postTags", # through PostTag unique combined key
                            backref='tag')


class Response(db.Model):
    """Class that cross references users' responses with corresponding posts"""

    __tablename__ = "responses"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))

    reply_author = db.Column(db.String(60),
                             nullable=False)

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'))

    response = db.Column(db.String(50000),
                         nullable=False)

  
    likes_reply = db.relationship(
        "Response",
        secondary="likes_reply",
        primaryjoin=(Like_reply.reply_id == id),
    )
 
    response_date = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )

    @classmethod
    def get_responses_by_post_id(cls, id):
        """Get all responses matching a post id"""

        data = cls.query.filter_by(user_id=id).all()
        return data
