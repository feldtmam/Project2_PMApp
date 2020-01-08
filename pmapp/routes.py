import os
from flask import render_template, url_for, flash, redirect, request, abort
from pmapp import app, db
from pmapp.forms import ResourcesForm, TaskForm, UpdateResourceForm
from pmapp.models import Resource, Task
import pandas as pd




resource_list=[]

all_resources = Resource.query.all()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

def save_marker_image(form_picture):
    marker_file = form_picture.filename
    marker_path = os.path.join(app.root_path, 'static/marker_pics', marker_file)
    form_picture.save(marker_path)
    return marker_path

@app.route("/resources", methods=['GET', 'POST'])
def resources():
    form = ResourcesForm()
    print('Resource count ', Resource.query.count()) # this will just print out in the terminal
    # just for testing to print all users to terminal
    for user in all_resources:
        #resource_list = 
        print(user.fullname)   
    if form.validate_on_submit():
        if form.marker_image.data:
            marker_image_file = save_marker_image(form.marker_image.data)
        flash(f'Resource {form.fullname.data} saved!', 'success')
        resource = Resource(fullname=form.fullname.data, department=form.department.data, allocation_percentage=form.allocation_percentage.data, marker_image=marker_image_file)
        db.session.add(resource)
        db.session.commit()
    return render_template('resources.html', title='Resources', form=form, resource_names=all_resources) #send the form and the list of resources to the template

@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        flash(f'Resource {form.task_description.data} saved!', 'success')
        #task = Task(project_title=form.project_title.data, parent_id=form.parent_id.data, status=form.status.data, task_description=form.task_description.data, start_date=form.start_date.data, end_date=form.end_date.data, resource_id=form.resource.data)
        task = Task(project_title=form.project_title.data, parent_id=form.parent_id.data, status=request.form.get('status'), task_description=form.task_description.data, start_date=form.start_date.data, end_date=form.end_date.data, resource_id=request.form.get('resource'))
        db.session.add(task)
        db.session.commit()
    return render_template('tasks.html', title='Tasks', form=form ) #passing the dummy data to the web page - removed posts=task

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f)
        #uncomment this when file contains all the required columns
        data_xls.to_sql(name='task', con=db.engine, if_exists='append',index=False)
        #return data_xls.to_html()
    return render_template('upload.html', title='Upload Excel File')