from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, TimeField
from wtforms import StringField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, URL
from wtforms_sqlalchemy.fields import QuerySelectField
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
        allow_blank=False,
        # blank_text=(u'Choose a teacher ...'),
        get_label='name')

    course = QuerySelectField(
        'course_id',
        query_factory=course_query,
        validators=[DataRequired()],
        allow_blank=False,
        get_label='name')

    tree = QuerySelectField(
        'tree_id',
        default="My tree",
        query_factory=tree_query,
        validators=[DataRequired()],
        allow_blank=False,
        get_label='name')

    course_date = DateField(
        'DatePicker',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    course_time = TimeField(
        'TimePicker',
        validators=[DataRequired()]
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
        'img_url',
        validators=[DataRequired(message="Enter URL Please"),
                    URL(message="Enter Valid URL Please.")]
    )


class TreeForm(FlaskForm):
    submit = SubmitField('Submit')

    name = StringField(
        'name', validators=[DataRequired()]
    )
    type = StringField(
        'type', validators=[DataRequired()],
    )
    location = StringField(
        'location', validators=[DataRequired()],
    )
    img_url = StringField(
        'img_url',
        validators=[DataRequired(message="Enter URL Please"),
                    URL(message="Enter Valid URL Please.")]
    )
