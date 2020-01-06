from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, DecimalField, DateField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date
#from pmapp import db, Resource


# def get_resource_list():
#     return db.session.query(Resource.fullname).all()

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
    status = SelectField('Status', choices=[('Select','Select'),('Not Started','Not Started'), ('Not Started','In Progress'), ('Not Started', 'Deferred'), ('Not Started','Completed')])
    task_description= StringField('Task Description',
                        validators=[DataRequired()])
    start_date = DateField('Start Date', default=date.today)
    end_date = DateField('End Date', default=date.today)
    # add code to populate dropdown list with full names from db
    resource = SelectField('Resource', choices=[('Select','Select'),('Bridgette','Bridgette'), ('Jack Stromberg', 'Jack Stromberg'), ('James DeCola','James DeCola'), ('Lauren Chavez','Lauren Chavez'),('Martie Feldtmann','Martie Feldtmann')])                   
    # resource = QuerySelectField(u'Resource',      
    #                            validators=[DataRequired()],
    #                            query_factory=get_resource_list)                   
    submit = SubmitField('Save Task')

class UpdateResourceForm(FlaskForm):
    fullname = StringField('Fullname',
                           validators=[DataRequired()])
    department = StringField('Department',
                        validators=[DataRequired()])
    allocation_percentage = StringField('Allocation %', validators=[DataRequired()])
    submit = SubmitField('Update Resource')