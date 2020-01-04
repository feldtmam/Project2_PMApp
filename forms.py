from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
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
    marker_image = FileField('Add Marker Image', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Save Resource')


class TaskForm(FlaskForm):
    project_title = StringField('Project Title',
                        validators=[DataRequired()])
    parent_id = DecimalField('Parent ID', validators=[DataRequired()])
    status = SelectField('Status', choices=[('NS','Not Started'), ('IP','In Progress'), ('DF', 'Deferred'), ('CP','Completed')])
    task_description= StringField('Task Description',
                        validators=[DataRequired()])
    start_date = DateField('Start Date', default=date.today)
    end_date = DateField('End Date', default=date.today)
    # add code to populate dropdown list with full names from db
    resource = SelectField('Resource', choices=[('TBD','0'), ('MF','1'), ('MM', '2'), ('DD','3')])                   
    submit = SubmitField('Save Task')

class UpdateResourceForm(FlaskForm):
    fullname = StringField('Fullname',
                           validators=[DataRequired()])
    department = StringField('Department',
                        validators=[DataRequired()])
    allocation_percentage = StringField('Allocation %', validators=[DataRequired()])
    submit = SubmitField('Update Resource')