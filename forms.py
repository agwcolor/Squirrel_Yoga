from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, SelectMultipleField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, AnyOf, URL
from wtforms_sqlalchemy.fields import QuerySelectField #whereshouldthisgo
from models import Teacher, Course, Tree


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

'''class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True)'''

def teacher_query():
    return Teacher.query

def course_query():
    return Course.query

def tree_query():
    return Tree.query

class EventForm(FlaskForm):
    submit = SubmitField('Submit')
    teacher = QuerySelectField(
        'teacher_id',
        query_factory=teacher_query,
        validators=[DataRequired()],
        allow_blank=True,
        #blank_text=(u'Choose a teacher ...'),
        get_label='name')

    course = QuerySelectField(
        'course_id',
        query_factory=course_query,
        validators=[DataRequired()],
        allow_blank=True,
        #blank_text=(u'Choose a course ...'),
        get_label='name')

    tree = QuerySelectField(
        'tree_id',
        default="My tree",
        query_factory=tree_query,
        validators=[DataRequired()],
        allow_blank=True,
        #blank_text=(u'Choose a tree location ...'),
        get_label='name')

    course_date = DateTimeField(
        'course_date',
        validators=[DataRequired()],
        default=datetime.today()
    )
    '''
    class EventForm(FlaskForm):
    submit = SubmitField('Submit')

    teacher_id = StringField(
        'teacher_id'
    )
    course_id = StringField(
        'course_id'
    )
    tree_id = StringField(
        'tree_id'
    )
    course_date = DateTimeField(
        'course_date',
        validators=[DataRequired()],
        default=datetime.today()
    )'''

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

class TreeForm(FlaskForm):
    submit = SubmitField('Submit')

    name = StringField(
        'name', validators=[DataRequired()]
    )
    tree_type = IntegerField(
        'type', validators=[DataRequired()]
    )
    tree_location = IntegerField(
        'location', validators=[DataRequired()]
    )
    img_url = StringField(
        'img_url', validators=[URL()]
    )