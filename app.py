"""Talk App"""


from news import get_news, get_news_2
import requests
from werkzeug.datastructures import ImmutableMultiDict

from flask_debugtoolbar import DebugToolbarExtension
import json
from models import (db,
                    connect_db,
                    User, Post,
                    Tag, Like,
                    Dislike,
                    Response,
                    Like_reply,
                    Dislike_reply,
                    SavedArticle)

from flask import (Flask,
                   jsonify,
                   session,
                   sessions,
                   g,
                   request,
                   render_template,
                   redirect,
                   flash,
                   url_for,
                   Blueprint)

from flask_mobility import Mobility

import os
import re

try:
    from keys import SECRET_KEY_keys, RECAPTCHA_PRIVATE_KEY_keys, RECAPTCHA_PUBLIC_KEY_keys
except:
    SECRET_KEY_keys="nokey"
    RECAPTCHA_PRIVATE_KEY_keys="nokey"
    RECAPTCHA_PUBLIC_KEY_keys="nokey"

from forms import (AddUser,
                   AddComment,
                   AddResponse,
                   LoginForm,
                   UpdateUser,)


from flask_restful import (Api,
                           Resource,
                           reqparse)

app = Flask(__name__)
Mobility(app)
api = Api(app)


# from flask_recaptcha import ReCaptcha
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PRIVATE_KEY_keys
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY_keys


# BEWARE that postgres:/// or postgresql:/// are now deprecated and will return dialect error
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', "postgresql:///talk")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY_keys)

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.testing = True
# debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)







@app.route("/")
def just_dev():
    return redirect(url_for("main_page"))


#############################################################################

errors = Blueprint('errors', __name__)


@app.errorhandler(Exception)
def server_error(err):
    """404 NOT FOUND page."""
    app.logger.exception(err)
    flash(f"{err}", "message label label-danger")
    # raise
    db.session.rollback()
    return render_template('404.html'), 404


@app.route("/talk")
def main_page():
    """List Users and show add form."""

    print("////////////////////////////////////////////////////")

    users = User.query.all()
    form = AddUser()
    user_auth = session.get("user_id", None)
    print(f"********************* user_auth = {user_auth}")

    saved_articles = None
    if ("user_id" in session):
        user_id = User.query.get(user_auth).id
        saved_articles = SavedArticle.query.filter_by(user_id=user_id).all()

    # n = get_news("top-headlines", "breaking-news")

    all_posts = Post.query.all()

    return render_template("talk_home.html",
                           users=users,
                           articles=news_api_req(),
                           all_posts=all_posts,
                           form=form,
                           User=User,
                           user_auth=user_auth,
                           Response=Response,
                           saved_articles=saved_articles)


@app.route("/talk/signup", methods=["POST", "GET"])
def add_user():
    """WTF version of add_user()"""

    print("-----------------------------------")

    form = AddUser()

    users = User.query.all()  # for the re-rendering
    all_posts = Post.query.all()

    if form.validate_on_submit():

        print("USER FORM VALIDATION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        name = form.name.data
        last_name = form.last_name.data
        img_url = form.img_url.data
        username = form.username.data
        password = form.password.data

        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f"name: {name}")
        print(f"last_name: {last_name}")
        print(f"img_url: {img_url}")
        print(f"username: {username}")
        print(f"password: {password}")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

        User.register(name=name, last_name=last_name,
                      img_url=img_url, username=username, password=password)

        return redirect(url_for("main_page"))
    else:
        print(f"--------------------------ADDING USER------------------------------------")
        return render_template("user_form.html",
                               users=users,
                               articles=news_api_req(),
                               User=User,
                               all_posts=all_posts,
                               form=form)
        
        


@app.route("/talk/signin", methods=["POST", "GET"])
def signin():
    """signing in"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        print(f"user::::::::::::::::::::::::::::::::::: {user}")
        print(f"password::::::::::::::::::::::::::::::: {password}")

        if user:
            all_posts = Post.query.all()
            session["user_id"] = user.id  # keep logged in
            users = User.query.all()
            user_auth = User.query.get_or_404(user.id)
            print(f"user_auth::::::::::::::::::::::::::::::: {user_auth}")

            return render_template("talk_home.html",
                                   users=users,
                                   articles=news_api_req(),
                                   all_posts=all_posts,
                                   form=form,
                                   currentuser=user,
                                   user_auth=user_auth,
                                   User=User,
                                   Response=Response)

        else:
            form.username.errors = ["WRONG NAME/PASSWORD"]

    return render_template("user_login.html", form=form)


@app.route("/talk/<int:user_id>", methods=["POST", "GET"])
def show_user(user_id):
    """Show info on a single user and allow them to post new comments"""
    if "user_id" not in session:
        flash("Please, log in first...", "alert alert-dark")
        return redirect("/")

    form = AddComment()
    users = User.query.all()
    user = User.query.get_or_404(user_id)

    # yes, needs to be called twice (due to try/except below)
    old_posts = Post.get_posts_by_id(user_id)

    if form.validate_on_submit():
        title = form.post_title.data
        post_content = form.post_content.data

        new_post = Post(
            user_id=user_id,
            post_author=user.full_name,
            post_title=title,
            post=post_content
        )

        db.session.add(new_post)

        try:
            db.session.commit()
        except Exception as e:
            err = e.orig
            flash(f"{err}", "message label label-danger")
            db.session.rollback()
            return render_template("user_blog.html", users=None, currentuser=user, old_posts=old_posts, form=form)

    # make sure to display the lastest values
    old_posts = Post.get_posts_by_id(user_id)
    return render_template("user_blog.html", users=users, User=User, currentuser=user, old_posts=old_posts, form=form)


@app.route("/talk/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user"""

    if "user_id" not in session:
        flash("You must be logged in to post!", "alert alert-dark")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    session_commit()

    users = User.query.all()
    return redirect(url_for("main_page"))


@app.route("/talk/edit/<int:user_id>", methods=["POST", "GET"])
def edit_user(user_id):
    """Method for editing a user's info and password"""

    print("*****************************************************--")
    if "user_id" not in session:
        flash("Please, log in first.", "alert alert-dark")
        return redirect("/")

    form = UpdateUser()
    users = User.query.all()  # for context re-rendering
    usr = User.query.get(user_id)
    all_posts = Post.query.all()

    # pre-populate the form:
    if request.method == 'GET':
        form.name.data = usr.name
        form.last_name.data = usr.last_name
        form.img_url.data = usr.img_url
        form.username.data = usr.username

    if form.validate_on_submit():

        print("USER FORM VALIDATION *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        name = form.name.data
        last_name = form.last_name.data
        img_url = form.img_url.data
        username = form.username.data
        old_password = form.old_password.data
        new_password = form.new_password.data
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f"name: {name}")
        print(f"last_name: {last_name}")
        print(f"img_url: {img_url}")
        print(f"username: {username}")
        print(f"password: {old_password}")
        print(f"password: {new_password}")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

        # authenticate old password
        user = User.authenticate(username, old_password)

        if user:
            User.update_user(user, name=name, last_name=last_name,
                             img_url=img_url, username=username, new_password=new_password, old_password=old_password)
            flash(f"User {name} {last_name} was updated",
                  "alert alert-primary")
        else:
            flash(f"User {name} {last_name} was NOT updated (incorrect password)",
                  "alert alert-primary")

        return redirect(url_for("main_page"))
    else:
        print(
            f"--------------------------EDITING USER------------------------------------")
        return render_template("edit_user_form.html", users=users, all_posts=all_posts, form=form, User=User, user=usr)


@app.route("/tags")
def get_tags():
    """list all existing tags"""


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    """API DELETE POSTS METHOD"""
    if "user_id" not in session:
        flash("Please, log in first.", "alert alert-dark")
        return redirect("/")

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    session_commit()
    return jsonify(message="deleted")


@app.route("/api/posts/like/<int:id>", methods=["POST"])
def like_post(id):
    """API LIKE POSTS METHOD"""
    print(f"**************************************************API LIKE POSTS METHOD***********************************************")

    nb_likes = Like.query.filter_by(post_id=id).count()
    print(f"********* NB LIKES = {nb_likes}")

    if "user_id" not in session:
        return jsonify(likes=nb_likes, state="loginrequired")

    user = User.query.get(session["user_id"])

    print(f"**********************************already_liked_by_user ?**************************************************")
    print(f"user = {user}")

    # see if in 'likes' table, there's a row with user_id = user.id and post_id = id
    l = Like.query
    already_liked_by_user = l.filter(
        Like.user_id == user.id, Like.post_id == id).first() != None

    print(
        f"********************************already_liked_by_user ? {already_liked_by_user}*********************************")

    if already_liked_by_user:
        return jsonify(likes=nb_likes, state="alreadyliked")
    else:
        newData = Like(user_id=user.id, post_id=id)
        db.session.add(newData)
        session_commit()

        nb_likes = Like.query.filter_by(post_id=id).count()  # update value

        return jsonify(likes=nb_likes)


@app.route("/api/posts/dislike/<int:id>", methods=["POST"])
def dislike_post(id):
    """API DISLIKE POSTS METHOD"""

    print(f"**************************************************API DISLIKE POSTS METHOD***********************************************")

    nb_dislikes = Dislike.query.filter_by(post_id=id).count()
    print(f"********* NB DISLIKES = {nb_dislikes}")

    if "user_id" not in session:
        return jsonify(dislikes=nb_dislikes, state="loginrequired")

    user = User.query.get(session["user_id"])

    print(f"**********************************already_disliked_by_user ?**************************************************")
    print(f"user = {user}")

    # see if in 'dislikes' table, there's a row with user_id = user.id and post_id = id
    l = Dislike.query
    already_disliked_by_user = l.filter(
        Dislike.user_id == user.id, Dislike.post_id == id).first() != None

    print(
        f"********************************already_disliked_by_user ? {already_disliked_by_user}*********************************")

    if already_disliked_by_user:
        return jsonify(dislikes=nb_dislikes, state="alreadydisliked")
    else:

        newData = Dislike(user_id=user.id, post_id=id)
        db.session.add(newData)
        session_commit()

        nb_dislikes = Dislike.query.filter_by(
            post_id=id).count()  # update value

        return jsonify(dislikes=nb_dislikes)

# /***********LIKES TO REPLIES***************************/


@app.route("/api/replies/<int:id>", methods=["DELETE"])
def delete_reply(id):
    """API DELETE REPLIES METHOD"""

    print("-----------DELETE A REPLY---------------")
    reply = Response.query.get_or_404(id)

    print(f"-----------DELETING REPLY {reply}---------------")
    db.session.delete(reply)
    session_commit()
    serialized = {"reply": "deleted"}
    return jsonify(message=serialized)


@app.route("/api/replies/like/<int:id>", methods=["POST"])
def like_reply(id):
    """API LIKE A REPLY METHOD"""
    print(f"**************************************************API LIKE A REPLY METHOD***********************************************")

    nb_likes = Like_reply.query.filter_by(reply_id=id).count()
    print(f"********* NB LIKES = {nb_likes}")

    if "user_id" not in session:
        return jsonify(likes=nb_likes, state="loginrequired")

    user = User.query.get(session["user_id"])

    print(f"**********************************already_liked_by_user ?**************************************************")
    print(f"user = {user}")

    # see if in 'likes' table, there's a row with user_id = user.id and post_id = id
    l = Like_reply.query
    already_liked_by_user = l.filter(
        Like_reply.user_id == user.id, Like_reply.reply_id == id).first() != None

    print(
        f"********************************already_liked_by_user ? {already_liked_by_user}*********************************")

    if already_liked_by_user:
        return jsonify(likes=nb_likes, state="alreadyliked")
    else:
        newData = Like_reply(user_id=user.id, reply_id=id)
        db.session.add(newData)
        session_commit()

        nb_likes = Like_reply.query.filter_by(
            reply_id=id).count()  # update value

        return jsonify(likes=nb_likes)


@app.route("/api/replies/dislike/<int:id>", methods=["POST"])
def dislike_reply(id):
    """API DISLIKE REPLIES METHOD"""

    print(f"**************************************************API DISLIKE A REPLY METHOD***********************************************")

    nb_dislikes = Dislike_reply.query.filter_by(reply_id=id).count()
    print(f"********* NB DISLIKES = {nb_dislikes}")

    if "user_id" not in session:
        return jsonify(dislikes=nb_dislikes, state="loginrequired")

    user = User.query.get(session["user_id"])

    print(f"**********************************already_disliked_by_user ?**************************************************")
    print(f"user = {user}")

    # see if in 'dislikes' table, there's a row with user_id = user.id and reply_id = id
    l = Dislike_reply.query
    already_disliked_by_user = l.filter(
        Dislike_reply.user_id == user.id, Dislike_reply.reply_id == id).first() != None

    print(
        f"********************************already_disliked_by_user ? {already_disliked_by_user}*********************************")

    if already_disliked_by_user:
        return jsonify(dislikes=nb_dislikes, state="alreadydisliked")
    else:

        newData = Dislike_reply(user_id=user.id, reply_id=id)
        db.session.add(newData)
        session_commit()

        nb_dislikes = Dislike_reply.query.filter_by(
            reply_id=id).count()  # update value

        return jsonify(dislikes=nb_dislikes)

# ***************************REPLY TO A POST****************************


@app.route("/api/reply/<int:post_id>", methods=["GET", "POST"])
def answer(post_id):
    """Create a new form and a reply linked to a specific post"""

    if "user_id" not in session:
        flash("You must be logged in to post!", "alert alert-dark")
        return redirect("/")

    # form = AddUser()
    form = AddResponse()
    users = User.query.all()
    all_posts = Post.query.all()

    post = Post.query.get_or_404(post_id)

    user = post.user_id

    if form.validate_on_submit():
        response = form.response.data
        author = User.query.get(session["user_id"]).name

        print(f"user id: {user}")
        new_reply = Response(user_id=user, post_id=post_id,
                             reply_author=author, response=response)

        db.session.add(new_reply)
        session_commit()

        return redirect(url_for("main_page"))

    post_id_form = post_id

    user_auth = session.get("user_id", None)

    return render_template("reply_form.html", form=form, post=post)


def session_commit():
    try:
        db.session.commit()
        print(f'COMMIT SUCCESSFUL')
    except Exception as e:
        err = e.orig
        flash(f"{err}", "message label label-danger")
        db.session.rollback()
        return redirect(url_for("main_page"))


@app.route("/talk/signout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")


@app.route("/api/flashloginfirst")
def login_required():
    print("******************loginrequired!****************")
    flash("Please, log in first...", "alert alert-dark")
    return jsonify(message="flashmessagesent")
    # return redirect(url_for("main_page"))


@app.route("/api/flashalreadyliked")
def already_liked():
    flash("You can't like a post twice!", "alert alert-dark")
    return redirect(url_for("main_page"))

# ############################################################################## NEWS API ####################################################################


# I use 2 different API's because their daily number of requests is limited in their respective
# free editions.


def news_api_req():

    articles = {}

    news = get_news("top-headlines", "breaking-news")
    if list(news.keys())[0] == "errors":
        """THE 2 API'S USE ONE (AND ONE ONLY) DIFFERENT KEY FOR THE IMAGE URL
        THIS FUNCTION MAKES SURE THEY BOTH HAVE THE SAME KEY
        TODO: SYSTEMATIZE HOMOGENEITY OF ALL KEYS... big project!
        """
        news = get_news_2()
        articles = news['articles']

        for dic in articles:
            print(
                f"*****************************************************************************")
            print(
                f"                             ARTICLES BEFORE KEY CHANGE                      ")
            print(f"{dic}")
            print(
                f"*****************************************************************************")

            v = dic['urlToImage']
            del dic['urlToImage']
            dic['image'] = v

            print(
                f"*****************************************************************************")
            print(
                f"                             ARTICLES WITH NEW KEY                           ")
            print(f"{dic}")
            print(
                f"*****************************************************************************")

        return articles

    else:
        articles = news['articles']
        return articles


print("APP.PY OK")

# ############################################################################## SAVE ARTICLES ####################################################################

# parser = reqparse.RequestParser()
# parser.add_argument('list', type=list)


@app.route("/api/article/save", methods=['GET', 'POST', 'OPTIONS'])
def save_article():
    """save a specific artice"""

    data = request.data
    data = data.decode('utf-8')  # convert bytes to string utf-8

    data = json.loads(data)  # convert string dict to dict

    title = data['title']
    url = data['url']

    print(f"*********************************************************")
    print()
    print(f"saving title: {title}")
    print(f"saving url: {url}")
    print()
    print(f"*********************************************************")

    if "user_id" not in session:
        # flash("Please, log in first.", "alert alert-dark") # now done by js with overlay
        return jsonify(message="loginrequired")

    userid = User.query.get(session["user_id"]).id

    print(f"*********************************************************")
    print()
    print(f"userid: {userid}")
    print()
    print(f"*********************************************************")

    # check entry doesn't already exist by comparing titles

    already_saved = False if SavedArticle.query.filter(
        SavedArticle.title.like(title)).all() == [] else True

    if (already_saved):
        return jsonify(message="alreadysaved")

    article = SavedArticle(user_id=userid, title=title, url=url)

    db.session.add(article)
    db.session.commit()

    return jsonify(message="saved")
