# THYTALK
https://www.thytalk.com 

## Description

* ThyTalk is a solcial media platform that allows user to:
    * Submit a post
    * Comment on news
    * Reply to a post
    * Search for news based on keywords
    * Like / unlike posts/comments/replies/news
    * Save news articles

* User flow
  * User must sign in/up: username, Name, Last Name, password - captcha
  * Search for news
  * Comment on news
  * Save articles
  * See other online users
  * Chat (not implemented yet)

## STACK

* Flask with Jinja templates
* Bootstrap 
* Javascript (for dynamic contents such as adding a comment)
* PostgreSQL m-2-m database

## API'S

### PUBLIC API'S

1. https://newsapi.org/v2/
2. https://gnews.io/api/v4/ 
   
   * NB: used alternatively whenever one has reached free usage limit

### PRIVATE API

* Base url = "/"

* queries: 
  <br>
    * "/search_news/{keyword}"
    * "/talk/signup" methods: "POST", "GET"
    * "/talk/signin" methods: "POST", "GET"
    * "/talk/signout" 
    * "/talk/post/{user_id}" methods: "POST", "GET"
    * "/talk/editpost/{post_id}" methods: "POST", "GET"
    * "/talk/post_news/{user_id}" methods: "POST"
    * "/talk/users/{user_id}" methods: "DELETE"
    * "/talk/edit/{user_id}" methods: "POST", "GET"
    * "/talk/userprofile/{user_id}"
  <br>
    * "/api/posts/{id}" methods: "DELETE"
    * "/api/posts/like/{id}" methods: "POST"
    * "/api/replies/{id}" methods: "DELETE"
    * "/api/replies/like/{id}" methods: "POST"
    * "/api/reply/{post_id}" methods: "GET", "POST"
  
    * "/api/flashloginfirst"
    * "/api/flashalreadyliked"
    * "/api/article/save" methods: "GET", "POST", "OPTIONS"
    * "/api/likearticle/" methods: "POST", "GET"

## REQUIREMENTS

alembic==1.9.1
aniso8601==9.0.1
asttokens==2.2.1
autopep8==1.7.0
backcall==0.2.0
bcrypt==4.0.1
blinker==1.5
botocore==1.27.91
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==2.1.1
click==8.1.3
cryptography==38.0.4
decorator==5.1.1
dnspython==2.2.1
ec2instanceconnectcli==1.0.2
email-validator==1.3.0
executing==1.1.1
Flask==2.2.2
Flask-Bcrypt==1.0.1
Flask-DebugToolbar==0.13.1
Flask-Login==0.6.2
Flask-Migrate==4.0.1
Flask-Mobility==1.1.0
Flask-ReCaptcha==0.4.2
Flask-RESTful==0.3.9
Flask-SQLAlchemy==2.5.1
Flask-WTF==1.0.1
greenlet==2.0.1
gunicorn==20.1.0
idna==3.4
importlib-metadata==5.0.0
ipython==8.5.0
itsdangerous==2.1.2
jedi==0.18.1
Jinja2==3.1.2
jmespath==1.0.1
Mako==1.2.4
MarkupSafe==2.1.1
matplotlib-inline==0.1.6
parso==0.8.3
pexpect==4.8.0
pickleshare==0.7.5
prompt-toolkit==3.0.31
psycopg2-binary==2.9.5
ptyprocess==0.7.0
pure-eval==0.2.2
pycodestyle==2.9.1
pycparser==2.21
Pygments==2.13.0
python-dateutil==2.8.2
pytz==2022.7
requests==2.28.1
six==1.16.0
SQLAlchemy==1.3 # Utlerior versions break on heroku and throw this error message:
\# "sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres"
stack-data==0.5.1
toml==0.10.2
traitlets==5.5.0
\# ufw @ https://launchpad.net/ufw/0.36/0.36/+download/ufw-0.36.tar.gz
urllib3==1.26.12
wcwidth==0.2.5
Werkzeug==2.2.2
WTForms==3.0.1
zipp==3.10.0
