import os
from flask import Flask, abort, json, jsonify
from models import setup_db, Actor, Movie
from flask_cors import CORS
#from flask_migrate import Migrate

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    #migrate = Migrate(app, db) #udacity help
    CORS(app)
    return app
app = create_app()


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
#  Controllers.
#----------------------------------------------------------------------------#

    
@app.route('/')
def get_greeting():
    excited = os.environ['EXCITED']
    greeting = "Bongo" 
    if excited == 'true': greeting = greeting + "!!!!!"
    return greeting
@app.route('/coolkids')
def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"

@app.route('/actors', methods=['GET'])
def get_actors():
    try:
        actors = Actor.query.order_by(Actor.id).all()
        data = []
        for actor in actors:
            data.append({
                "id": actor.id,
                "age": actor.age,
                "name": actor.name
            })
        print(data)
        return jsonify({
            'success': True,
            'count': len(actors),
            'data': data
        })
    except Exception:
        abort(422)


if __name__ == '__main__':
    app.run()