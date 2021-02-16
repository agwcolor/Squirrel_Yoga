Squirrel Yoga ---- <Work in Progress - not completed>
-------------

## Introduction

Squirrel Yoga is a site for teachers and admins to create/modify/delete and manage courses, events, locations (trees) .  The general public can view them.

## Overview
Tables : Teachers, Events, Courses, Trees
Front-end : Flask Templates

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

### 2. Frontend Dependencies
None - Bootstrap 4 accessed via URL
```
## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. .
                    "python app.py" to run after installing dependences
  ├── models.py *** SQLAlchemy Models
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py ***  forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── /forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` in  `models.py`.
* Controllers are located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` --  Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` -- (Missing functionality.) Defines the data models that set up the database tables.
* `config.py` -- N/A --- Using environment variables -----Stores configuration variables and instructions, separate from t  he main application code. 
* `flask db migrate` should work, and populate  local postgres database with properly configured tables for this application's objects, including proper columns, column data types, constraints, defaults, and relationships that completely satisfy the needs of this application. The proper type of relationship between venues, artists, and shows should be configured.


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
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

