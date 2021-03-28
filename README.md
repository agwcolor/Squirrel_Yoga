Squirrel Yoga ---- <Work in Progress - not completed>
-------------

## Introduction

Squirrel Yoga is a full-stack website where users can create/modify/delete and manage teachers, courses, events, and tree locations.  

## Overview
This project is an implentation of an app using a Model View Controller architecture to store and retrieve data via an API written in Python usinpwdg Flask. Authentication using Auth0, a 3rd party authentication service and tests written using unittest are also required. The final project is deployed on Heroku.  Although a Front-End was not required, I included a light-weight one using Jinja Templates so that I could learn how to do this and also have a convenient visual interface and to complete a full-stack app that anyone can use.

## Authentication
There are 4 anticipated users (roles) configured using Auth0 3rd party service:
* Anyone -- can view (GET) the website
* assistant -- can patch:teachers, patch:courses, patch:trees
* director -- can patch:teachers, patch:courses, patch:trees
post:teachers, post:courses, delete:teachers, delete:course
* owner -- can patch:teachers, patch:courses, patch:trees
post:teachers, post:courses, delete:teachers, delete:course
post:tree, post:event, delete:tree, delete:event

The web page should show an alert when an action is not allowed by the currently logged in user.  The home page should indicate who is currently logged in or if nobody is logged in.

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
│   └── squirrelsquare.jpg
├── templates
│   ├── base.html
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

DATABASE_URL='yourpostgresdatabaseurl'
SECRET_KEY='yourflasksecretkey'
AUTH0_CALLBACK_URL='yourauth0callbackurl'
AUTH0_CLIENT_ID='yourauth0clientid'
AUTH0_CLIENT_SECRET='yourauth0clientsecret'
export AUTH0_DOMAIN='yourauth0domain'
export AUTH0_AUDIENCE='yourauth0audience'


*  `models.py` -- defines the data models that set up the database tables. (the Models in this project are : Teachers, Events, Courses, Trees.) Loosely based on the structure of the Fyyr app project models.
* `app.py` --  main app file. Defines the routes that match the user’s URL and the controllers which handle data and render views to the user.
* `form.py` -- contains forms definitions using WFT_form, a built-in module in flask for designing forms, and WTForms library for form validation and rendering.
* `templates/` -- where the web frontend jinja templates are located. Templates are built based on the controllers (Flask enpoints) in `app.py`
* `templates/forms` -- where the web frontend jinja form templates are located. Form validation and definitions are defined in `forms.py`

* `requirements.txt` -- Lists all of the libraries required for this app to run. To install them : Create a virtual enviromnent, then install by running 'pip3 install -r `requirements.txt` '
* `migrations/` -- Alembic database migrations folder
* `flask db migrate` -- can be used to populate a local postgres database with properly configured tables and relationships for application  objects, including columns, column data types, constraints, and defaults.
* `auth/auth.py` -- handles checking authentication requirements for endpoints defined in `app.py` and verifying with Auth0 3rd party service that JWTs are valid. Most of this is boilerplate code used from the Coffeeshop project. However, significant modifications had to be made to work with Jinja templates to reflect the current user and login session.
* `tests.py` --  Note : The unit tests were to be written using the built in Python unittest library as required. It turns out that this was challenging to do because the front and backend is tightly coupled and I was unable to return json responses but had to test via returned & rendered templates instead.
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
python3 app.py    - or -  flask run
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

