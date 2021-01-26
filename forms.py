from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, SelectMultipleField, DateTimeField, SubmitField
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

moves_choices = [
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
        default=datetime.today()
    )

class CourseForm(FlaskForm):
    submit = SubmitField('Submit')

    name = StringField(
        'name', validators=[DataRequired()]
    )
    course_level = IntegerField(
        'course_level', validators=[DataRequired()]
    )
    img_url = StringField(
        'img_url', validators=[URL()]
    )

class TeacherForm(FlaskForm):
    submit = SubmitField('Submit')

    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    temperament = StringField(
        'temperament', validators=[DataRequired()],
    )
    moves = SelectMultipleField(
        'moves', validators=[DataRequired()],
        choices=moves_choices
    )
    img_url = StringField(
        'img_url', validators=[URL()]
    )