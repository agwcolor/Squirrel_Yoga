Squirrel Yoga ---- <Work in Progress - not completed>
-------------

## Introduction

Squirrel Yoga is a full-stack website capstone project built using Flask, postgres, SQLAlchemy ORM, and Auth0 for authentication. Users can create/modify/delete and manage teachers, courses, events, and tree locations depending on the authorization settings.  The website theme was inspired by all of the sqirrels I saw outside stretching and cavorting during lockdown.

#### Image attributions on deployed app

Squirrel images were taken by me. Other images are provided thanks to the photographers on Unsplash : @niko_photos, Debby Hudson (hudsoncrafted.myportfolio.com), Cristina Anne Costello, Rene Cadenas

## Overview
This project is an implentation of an app using a Model-View-Controller architecture to store and retrieve data via an API written in Python using Flask. Authentication is implemented using Auth0, a 3rd party authentication service. Tests are written using unittest. The final project is deployed on Heroku.  Although a Front-End was not required, I included a light-weight one using Jinja Templates so that I could learn how to do this and also to have a convenient visual interface for a full-stack application that anyone can use.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
The tech stack includes:
 * **virtualenv** for creating isolated Python environments
 * **SQLAlchemy ORM** our ORM library of choice
 * **PostgreSQL**  our database of choice
 * **Python3** and **Flask** our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

You can download and install the dependencies mentioned above using `pip` as:
```
pip3 install virtualenv
pip3 install SQLAlchemy
pip3 install postgres
pip3 install Flask
pip3 install Flask-Migrate
```

### 2. Frontend Dependencies
* Flask Template Libraries and WTForms (All are already listed in requirements.txt)
* Bootstrap 4 styles are accessed accessed via URL and do not need to be installed
```
## Project Structure
├── Procfile
├── README.md
├── app.py
├── auth
│   ├── __init__.py
│   ├── auth.py
├── forms.py
├── manage.py
├── migrations/
├── models.py
├── requirements.txt
├── setup.sh
├── static
│   ├── 2squirrel_sm.jpg
│   ├── arrow_copy.jpg
│   ├── base.css
│   ├── piano.png
│   ├── squirrel_basic.jpg
│   ├── Octocat.png
│   ├── favicon.ico
│   ├── walnut_haci-elmas-unsplash.jpg
│   └── squirrelsquare.jpg
├── templates
│   ├── base.html
│   ├── error.html
│   ├── courses.html
│   ├── dashboard.html
│   ├── events.html
│   ├── forms
│   │   ├── add_course.html
│   │   ├── add_event.html
│   │   ├── add_teacher.html
│   │   ├── add_tree.html
│   │   ├── edit_course.html
│   │   ├── edit_event.html
│   │   ├── edit_teacher.html
│   │   └── edit_tree.html
│   ├── home.html
│   ├── index.html
│   ├── logged_out.html
│   ├── show_course.html
│   ├── show_event.html
│   ├── show_teacher.html
│   ├── show_tree.html
│   ├── teachers.html
│   └── trees.html
├── tests.py
  ```


Folder & File Descriptions :

* `setup.sh` -- I used environment variables to store  applicaton and configuration variables that should remain hidden. You will need to define these yourself if you want to build this app locally and make sure they are available to your app, using your favorite environment variable storage method. (For deployment, these variables are manually configured on Heroku). 

Note: Replace the placeholder values!
```
DATABASE_URL='yourpostgresdatabaseurl'
SECRET_KEY='yourflasksecretkey'
AUTH0_CALLBACK_URL='yourauth0callbackurl'
AUTH0_CLIENT_ID='yourauth0clientid'
AUTH0_CLIENT_SECRET='yourauth0clientsecret'
AUTH0_DOMAIN='yourauth0domain'
AUTH0_AUDIENCE='yourauth0audience'
```

*  `models.py` -- defines the data models that set up the database tables. (the Models in this project are : Teachers, Events, Courses, Trees.) Loosely based on the structure of the Fyyr app project models.
* `app.py` --  main app file. Defines the routes that match the user’s URL and the controllers which handle data and render views to the user.
* `form.py` -- contains forms definitions using WFT_form, a built-in module in flask for designing forms, and WTForms library for form validation and rendering.
* `templates/` -- where the web frontend Jinja templates are located. Templates are built based on the controllers (Flask enpoints) in `app.py`
* `templates/forms` -- where the web frontend Jinja form templates are located. Form validation and definitions are defined in `forms.py`

* `requirements.txt` -- Lists all of the libraries required for this app to run. To install them : Create a virtual enviromnent, then install by running 'pip3 install -r `requirements.txt` '
* `migrations/` -- Alembic database migrations folder
* `flask db migrate` -- can be used to populate a local postgres database with properly configured tables and relationships for application  objects, including columns, column data types, constraints, and defaults.
* `auth/auth.py` -- handles checking authentication requirements for endpoints defined in `app.py` and verifying with Auth0 3rd party service that JWTs are valid. Most of this is boilerplate code used from the Coffeeshop project. However, significant modifications had to be made to work with Jinja templates to reflect the current user and login session.
* `tests.py` --  Note : The project rubric instructed us to use Python unittest library. It turns out that this was challenging to do because the front and backend is tightly coupled and I was unable to return json responses but had to test via returned & rendered templates instead. However, rendered json can be returned in if that section of the code is uncommented and the 'render template' portion commented out.
* `Procfile` -- for Heroku deployment. Used to run the app using gunicorn (WSGI http server) on Heroku


## Development Setup
1. **Download the project starter code locally**
```
git clone https://github.com/agwcolor/Squirrel_Yoga.git
cd /starter_code 
```

2. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

3. **Install the dependencies:**
```
pip install -r requirements.txt
```

4. **Run the development server:**
```
export FLASK_APP=app.py
export FLASK_ENV=development
python3 app.py    - or -   flask run
```

6. **Verify on the Browser**<br>
Navigate to project homepage ```http://127.0.0.1:5000/``` or ```http://localhost:5000``` 

## Authentication - RBAC behavior
This application uses the [Auth0](https://auth0.com/)
 authentication and authorization (identity management) platform.
See `/auth/auth.py` which uses a combination of the Coffeeshop project auth boilerplate, AUTH0 boilerplate for requires_auth() in `app.py`, as well as some auth to work with Jinja templates.

There are 4 anticipated users (roles) configured using Auth0 3rd party service:
* Anyone -- can view (GET)
* assistant -- can EDIT -- patch:teachers, patch:courses, patch:trees, patch:events
* director -- can EDIT / ADD -- patch:teachers, patch:courses, patch:trees, patch:events
post:teachers, post:courses, post:trees, post: events
* owner -- can EDIT / ADD / DELETE -- patch:teachers, patch:courses, patch:trees
post:teachers, post:courses, post:trees, post:events
delete:teachers, delete:courses, delete:trees, delete:events

The web page should show an alert when an action is not allowed by the currently logged in user.
The home page should indicate who is currently logged in or if nobody is logged in.

## API - Endpoints

The Squirrel Yoga API is a RESTful web service. It uses JSON-encoded responses and HTTP response codes. 
Since I created a Jinja front-end for this particular implementation of the project, no json is "returned" and templates are returned and rendered instead. 
However, the json does exsist and is commented out in the code and can be used as a return instead if you wanted to decouple the code from the front end.

It has 19 endpoints in 4 main categories: Teachers, Courses, & Trees, Events summarized here:

TEACHERS:
- GET '/teachers'
- GET '/teachers/:id'
- POST '/teachers/add'
- PATCH '/teachers/:id/edit'
- DELETE '/teachers/:id'

COURSES:
- GET '/courses'
- GET '/courses/:id'
- POST '/courses/add'
- PATCH '/courses/:id/edit'
- DELETE '/courses/:id'

TREES:
- GET '/trees'
- GET '/trees/:id'
- POST '/trees/add'
- PATCH '/trees/:id/edit'
- DELETE '/trees/:id'

EVENTS:
- GET '/events'
- POST '/events/add'
- PATCH '/events/:id/edit'
- DELETE '/events/:id'


### TEACHERS
GET '/teachers' <br>
- Fetches a list of teachers
- Request arguments: None
- Curl sample: ```curl "http://127.0.0.1:5000/teachers"```
- Returns:
```
{
  "count": 22,
  "data": [
    {
      "age": 7,
      "id": 1,
      "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,e_sharpen:100,w_360/v1611551630/sleepy_squirrel_ooxr6n.jpg",
      "moves": ["slowly", "dangle"],
      "name": "chibbibbity",
      "temperament": "clear-eyed"
    },
    {
      "age": 1,
      "id": 2,
      "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611551632/squirrel_stretch_kcwfmw.jpg",
      "moves": ["fly", "skip", "scratch"],
      "name": "sodoro",
      "temperament": "edgy"
    },
    
    ...

  ],
  "success": true
}
```

GET '/teachers/:id'
- Fetches an individual teacher
- Request arguments: teacher id
- Curl sample: ```curl "http://127.0.0.1:5000/teachers/1"```
- Returns:
```
{
  "data": [
    {
      "age": 7,
      "id": 1,
      "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,e_sharpen:100,w_360/v1611551630/sleepy_squirrel_ooxr6n.jpg",
      "moves": ["slowly", "dangle"],
      "name": "chibbibbity",
      "past_events": [
        {
          "course_date": "Mon, 15 Feb 2021 00:00:00 GMT",
          "course_id": 2,
          "course_name": "slink around",
          "tree_id": "2,
          "tree_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
          "tree_location": "backyard",
          "tree_name": "Nutter Heaven",
          "tree_type": "Walnut"
        },

        ...

        {
          "course_date": "Wed, 10 Feb 2021 22:33:04 GMT",
          "course_id": 1,
          "course_name": "bounce around",
          "tree_id":3,
          "tree_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
          "tree_location": "over yonder",
          "tree_name": "Pricly Haven",
          "tree_type": "Holly"
        }
      ],
      "past_events_count": 4,
      "temperament": "clear-eyed",
      "upcoming_events": [
        {
          "course_date": "Tue, 15 Mar 2022 00:00:00 GMT",
          "course_id": 3,
          "course_name": "scratch & sniff",
          tree_id":3,
          "tree_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
          "tree_location": "pasture",
          "tree_name": "Nutter Tiny",
          "tree_type": "Walnut"
        }
      ],
      "upcoming_events_count": 1
    }
  ],
  "success": true
}

```


POST '/teachers/add'
- Adds a teacher
- Request Arguments: teacher name text, age number, temperament, and moves
- Curl sample :
```
    curl http://127.0.0.1:5000/teachers/add
    -X POST
    -H "Content-Type: application/json"
    -d '{"name":"rocky","age":2, "temperament":"sly", "moves":["outhere","highbounce","horizontal fling"], "img_url":"https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"}'
```
- Returns : teacher.id


```
{
  "created": 25,
  "success": true
}
```

PATCH '/teachers/:id/edit'
- Modify a teacher
- Request Arguments: teacher name text, age number, temperament, and moves
- Curl sample : 
```
    curl http://127.0.0.1:5000/teachers/2/edit
    -X PATCH
    -H "Content-Type: application/json"
    -d '{"name":"rocky","age":2, "temperament":"sly", "moves":["outhere","highbounce","horizontal fling"], "img_url":"https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"}'
```
- Returns : teacher.id, teacher.name, teacher.moves


```
{
    "success": True,
    "modidifed": 3,
    "name": "rocky",
    "moves": ["outhere","highbounce","horizontal fling"]
}
```


DELETE '/teachers/:id'
- Deletes a teacher based on id
- Request arguments : id: id of teacher to be deleted 
- Curl sample : ```curl -X DELETE "http://127.0.0.1:5000/teachers/24"```
- Returns : deleted: id of the teacher that was deleted
```
{
  "deleted": 24,
  "success": true
}
```

### COURSES
GET '/courses' <br>
GET '/courses'
- Fetches a list of courses
- Request arguments: None
- Curl sample: ```curl "http://127.0.0.1:5000/courses"```
- Returns:
```
{
  "count": 10,
  "data": [
    {
      "course_id": 2,
      "course_level": 10,
      "course_teachers": [
        { "teacher_id": 1, "teacher_name": "chibbibbity" },
        { "teacher_id": 3, "teacher_name": "pongo" },
        { "teacher_id": 11, "teacher_name": "Footie" }
      ],
      "course_name": "slink around"
    },
    {
      "course_id": 3,
      "course_level": 4,
      "course_teachers": [
        { "teacher_id": 1, "teacher_name": "chibbibbity", "course_date":"2021-02-10 22:21:01" },
        { "teacher_id": 1, "teacher_name": "chibbibbity", "course_date":"2021-03-10 22:21:01" },
        { "teacher_id": 5, "teacher_name": "waz", "course_date":"2021-04-10 22:21:01" },
        { "teacher_id": 5, "teacher_name": "waz", "course_date":"2021-05-10 22:21:01" },
        { "teacher_id": 4, "teacher_name": "rocky", "course_date":"2021-06-10 22:21:01" }
      ],
      "course_name": "scratch & sniff"
    },

    ...

  ],
  "success": true
}
```

GET '/courses/:id'
- Fetches an individual course
- Request arguments: course id
- Curl sample: ```curl "http://127.0.0.1:5000/courses/1"```
- Returns:
```
{
  "data": [
    {
      "course_level": 2,
      "id": 1,
      "name": "bounce around",
      "past_events": [
        {
          "course_date": "Wed, 10 Feb 2021 22:21:01 GMT",
          "teacher_id": 3,
          "teacher_name": "pongo",
          "tree_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
          "tree_location": "over yonder",
          "tree_id": 1,
          "tree_name": "Pricly Haven",
          "tree_type": "Holly"
        },

        ...

        {
          "course_date": "Thu, 25 Feb 2021 20:36:30 GMT",
          "teacher_id": 2,
          "teacher_name": "sodoro",
          "tree_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
          "tree_location": "center divider",
          "tree_id": 1,
          "tree_name": "Acorn Fun",
          "tree_type": "Oak"
        }
      ],
      "past_events_count": 13,
      "upcoming_events": [],
      "upcoming_events_count": 0
    }
  ],
  "success": true
}


```

POST '/courses/add'
- Adds a course
- Request Arguments: course name text, course level
- Curl sample :
    ```curl http://127.0.0.1:5000/courses/add```
    -X POST
    -H "Content-Type: application/json"
    -d '{"name":"Dangle","course_level":5"}'
- Returns : course.id


```
{
  "created": 25,
  "success": true
}
```

PATCH '/courses/:id/edit'
- Modify a course
- Request Arguments: course name text, course level
- Curl sample :
    ```curl http://127.0.0.1:5000/courses/2/edit
    -X PATCH
    -H "Content-Type: application/json"
    -d '{"name":"Dangle","course_level":5"}'```
- Returns : course.id, course.name, course.level


```
{
    "success": True,
    "modidifed": 2,
    "name": "Dangle",
    "course_level": 5
}
```


DELETE '/courses/:id'
- Deletes a course based on id
- Request arguments : id: id of course to be deleted
- Curl sample : ```curl -X DELETE "http://127.0.0.1:5000/courses/2```
- Returns : deleted: id of the course that was deleted
```
{
  "deleted": 2,
  "success": true
}
```

### TREES
GET '/trees' <br>
GET '/trees'
- Fetches a list of tree locations.
- Request arguments: None
- Curl sample: ```curl "http://127.0.0.1:5000/trees"```
- Returns:
```
{
  "count": 5,
  "data": [
    {
      "id": 1,
      "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
      "name": "Pricly Haven",
      "tree_location": "over yonder",
      "tree_type": "Holly"
    },
    {
      "id": 2,
      "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
      "name": "Nutter Heaven",
      "tree_location": "backyard",
      "tree_type": "Walnut"
    },

    ...

    {
      "id": 5,
      "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
      "name": "Pokey",
      "tree_location": "yonder park",
      "tree_type": "Cedar"
    }
  ],
  "success": true
}

```

GET '/trees/:id'
- Fetches an individual tree
- Request arguments: tree id
- Curl sample: ```curl "http://127.0.0.1:5000/trees/1"```
- Returns:
```
{
  "data": [
    {
      "id": 1,
      "name": "Pricly Haven",
      "past_events": [
        {
          "course_date": "Wed, 10 Feb 2021 22:21:01 GMT",
          "course_id": 1,
          "course_level": 2,
          "course_name": "bounce around",
          "teacher_id": 3,
          "teacher_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_thumb,e_sharpen:100,q_100,r_4,w_360/v1611551628/squirrel_flat_zvhttz.jpg",
          "teacher_name": "pongo"
        },

        ...

        {
          "course_date": "Wed, 10 Feb 2021 22:33:04 GMT",
          "course_id": 1,
          "course_level": 2,
          "course_name": "bounce around",
          "teacher_id": 6,
          "teacher_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611551630/squirrel_tree_h5jfx8.jpg",
          "teacher_name": "barumbo"
        }
      ],
      "past_events_count": 9,
      "tree_img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg",
      "tree_location": "over yonder",
      "tree_type": "Holly",
      "upcoming_events": [],
      "upcoming_events_count": 0
    }
  ],
  "success": true
}



```

POST '/trees/add'
- Adds a tree
- Request Arguments: tree name text, type, location, and image url
- Curl sample :
    ```curl http://127.0.0.1:5000/trees/add
    -X POST
    -H "Content-Type: application/json"
    -d '{"name":"Figgy","type": "Fig", "location": "Scary Dog's Garden"}'
    ```
- Returns : tree.id


```
{
  "created": 2,
  "success": true
}
```

PATCH '/trees/:id/edit'
- Modify a tree
- Request Arguments: tree name, type, location
- Curl sample :
    ```curl http://127.0.0.1:5000/trees/2/edit
    -X PATCH
    -H "Content-Type: application/json"
    -d '{"name":"Figgy","type": "Fig", "location": "Scary Dog's Garden"}'
    ```
- Returns : 


```
{
    "success": True,
    "modidifed": 4,
    "name": "Figgy",
    "type": "Fig",
    "location": "Scary Dog's Garden",
    "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg"
}
```


DELETE '/trees/:id'
- Deletes a tree based on id
- Request arguments : id: id of tree to be deleted
- Curl sample : ```curl -X DELETE "http://127.0.0.1:5000/trees/4```
- Returns : deleted: id of the question that was deleted
```
{
  "deleted": 4,
  "success": true
}
```

### EVENTS
GET '/events' <br>
- Fetches a list of events and their details
- Request arguments: None
- Curl sample: ```curl "http://127.0.0.1:5000/events"```
- Returns:
```
{
  "count": 36,
  "data": [
    {
      "course_date": "Wed, 15 Jan 2020 00:00:00 GMT",
      "course_id": 1,
      "course_name": "bounce around",
      "event_id": 24,
      "teacher_id": 11,
      "teacher_name": "Footie",
      "tree_id": 5,
      "tree_name": "Pokey"
    },
    {
      "course_date": "Mon, 10 Feb 2020 22:50:04 GMT",
      "course_id": 1,
      "course_name": "bounce around",
      "event_id": 29,
      "teacher_id": 1,
      "teacher_name": "chibbibbity",
      "tree_id": 2,
      "tree_name": "Nutter Heaven"
    },

    ...

    {
      "course_date": "Sun, 11 Feb 2024 20:05:02 GMT",
      "course_id": 3,
      "course_name": "scratch & sniff",
      "event_id": 31,
      "teacher_id": 4,
      "teacher_name": "rocky",
      "tree_id": 3,
      "tree_name": "Nutter Tiny"
    }
  ],
  "success": true
}

```

POST '/events/add'
- Adds an event
- Request Arguments: teacher id, course id, tree id (autopopulated dropdown in form), date
- Curl sample : 
```
    curl http://127.0.0.1:5000/events/add
    -X POST
    -H "Content-Type: application/json"
    -d '{"teacher_id":2,"course_id":2,"tree_id":2, "date":"2021-03-31 22:36:28"}'
```
- Returns : teacher.id


```
{
  "created": 25,
  "success": true
}
```

PATCH '/events/:id/edit'
- Modify an event
- Request Arguments: teacher, course, tree, course date - (teacher_id, course_id, tree_id are autopopulated in the form so the user doesn't need to know the id number.)
- Curl sample : 
```
    curl http://127.0.0.1:5000/events/2/edit
    -X PATCH
    -H "Content-Type: application/json"
    -d '{"teacher_id":2,"course_id":2,"tree_id":2, "course_date":"2021-03-31 22:36:28"}'
    ```
- Returns : 


```
{
    "success": True,
    "modidifed": 2,
    "event_date": "2021-03-31 22:36:28"
}
```


DELETE '/events/:id'
- Deletes an event based on id
- Request arguments : id of event to be deleted 
- Curl sample : ```curl -X DELETE "http://127.0.0.1:5000/events/24```
- Returns : deleted: id of the event that was deleted
```
{
  "deleted": 24,
  "success": true
}
```



## Testing
To run the tests, run
```
python tests.py
```

## Deployment to Heroku
General workflow :
- Create Heroku account and install cli.
- Create app
```
heroku create hello-potato
```
- Upload code to app :
```
git push heroku main
```
- Add postgresql database addon
```
heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
```
- Using your Heroku dashboard, add any application configuration variables. You will see that the database is already configured.
- Run migrations :
```
heroku run python manage.py db upgrade --app name_of_your_application
```
- Upload local postgres data if you like, by first exporting the data to an outfile, then importing it using heroku cli.
```
pg_dump dbname > outfile
heroku pg:psql DATABASE_URL --app name_of_your_app < outfile
```
Useful commands :
``` heroku run bash ``` to see if files are there. ```heroku pg:psql``` to see your tables in postgres.





