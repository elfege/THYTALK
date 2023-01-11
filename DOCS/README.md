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

