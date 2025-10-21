from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

class NewProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[
        DataRequired(),
        Length(max=200)
    ])
    author_name = StringField('Your Name', validators=[
        DataRequired(),
        Length(max=100)
    ])
    description = TextAreaField('Project Description', validators=[
        DataRequired()
    ])


class CommentForm(FlaskForm):
    student_name = StringField('Your Name', validators=[
        DataRequired(),
        Length(max=100)
    ])
    comment_text = TextAreaField('Comment', validators=[
        DataRequired()
    ])
    parent_comment_id = HiddenField()
    quoted_text = TextAreaField('Quoted Text')
