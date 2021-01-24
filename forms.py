from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SelectMultipleField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, AnyOf, URL


tree_type = [
            ('Holly', 'Holly'),
            ('Walnut', 'Walnut'),
            ('Oak', 'Oak'),
            ('Cedar', 'Cedar'),
            ('Bush', 'Bush'),
            ('Poplar', 'Poplar'),
            ('Aspen', 'Aspen'),
        ]

tree_location = [
    ('over yonder', 'over yonder'),
    ('backyard', 'backyard'),
    ('pasture', 'pasture'),
    ('center divider', 'center divider'),
    ('yonder park', 'yonder park'),
    ('scary cave', 'scary cave')
]

move_choices = [
            ('slowly', 'slowly'),
            ('dangle', 'dangle'),
            ('hang', 'hang'),
            ('fly', 'fly'),
            ('skip', 'skip'),
            ('scratch', 'scratch'),
            ('sleepy', 'sleepy'),
        ]

class EventForm(FlaskForm):
    teacher_id = StringField(
        'teacher_id'
    )
    event_id = StringField(
        'event_id'
    )
    tree_id = StringField(
        'tree_id'
    )
    course_date = DateTimeField(
        'course_date',
        validators=[DataRequired()],
        default= datetime.today()
    )

class CourseForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    tree = SelectField(
        'tree', validators=[DataRequired()],
        choices=tree_type
    )
    location = StringField(
        'location', validators=[DataRequired()],
        choices=tree_location
    )
    image_link = StringField(
        'image_link'
    )
    website = StringField(
        'website'
    )


class TeacherForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = StringField(
        'age', validators=[DataRequired()]
    )
    temperament = SelectField(
        'temperament', validators=[DataRequired()],
    )
    moves = StringField(
        'moves', validators=[DataRequired()],
        choices=moves_choices
    )
    image_link = StringField(
        'image_link'
    )
    '''website = StringField(
        'website'
    )'''