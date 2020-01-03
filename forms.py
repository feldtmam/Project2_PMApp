from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, DateField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date


class ResourcesForm(FlaskForm):
    fullname = StringField('Fullname',
                           validators=[DataRequired()])
    department = StringField('Department',
                        validators=[DataRequired()])
    allocation_percentage = StringField('Allocation %', validators=[DataRequired()])
    submit = SubmitField('Save Resource')


class TaskForm(FlaskForm):
    project_title = StringField('Project Title',
                        validators=[DataRequired()])
    task_id = DecimalField('Task ID', validators=[DataRequired()])
    status = SelectField('Status', choices=[('NS','Not Started'), ('IP','In Progress'), ('DF', 'Deferred'), ('CP','Completed')])
    task_description= StringField('Task Description',
                        validators=[DataRequired()])
    start_date = DateField('Start Date', default=date.today)
    end_date = DateField('End Date', default=date.today)
    # add code to populate dropdown list with full names from db
    resource = SelectField('Resource', choices=[('TBD','Not Selected'), ('MF','Martie Feldtmann'), ('MM', 'Mickey Mouse'), ('DD','Donald Duck')])                   
    submit = SubmitField('Save Task')