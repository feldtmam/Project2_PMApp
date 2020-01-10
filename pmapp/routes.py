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

@app.route("/resources/<int:resource_id>", methods=['GET', 'POST']) #pass the resource id variable into the  route to display the specific record
def update_resource(resource_id):
    update_resource = Resource.query.get_or_404(resource_id) #this will get the resource record, or if it does not exist, show 404 error
    form = UpdateResourceForm()
    if form.validate_on_submit():
        update_resource.fullname = form.fullname.data     
        update_resource.department = form.department.data
        update_resource.allocation_percentage = form.allocation_percentage.data 
        db.session.commit()
        flash('The resource has been updated!', 'success')
        return redirect(url_for('resources'))
    elif request.method == 'GET':
        form.fullname.data = update_resource.fullname
        form.department.data = update_resource.department        
        form.allocation_percentage.data = update_resource.allocation_percentage
    #form.marker_image.data = update_resource.marker_image
    return render_template('update_resource.html', title=update_resource.fullname, form=form)

@app.route("/tasks/update_task/<task_id>", methods=['GET', 'POST'])
def update_tasks(task_id):
    update_task = Task.query.get_or_404(task_id)
    form = TaskForm()
    if form.validate_on_submit():
        update_task.project_title = form.project_title.data     
        update_task.parent_id = form.parent_id.data
        #new_status = request.values.get('status')
        #update_task.status = new_status
        update_task.status = form.status.data
        update_task.task_description = form.task_description.data 
        update_task.start_date = form.start_date.data 
        update_task.end_date = form.end_date.data 
        update_task.resource_id = form.resource.data 
        db.session.commit()
        flash('The task has been updated!', 'success')
        return redirect(url_for('tasks'))
    elif request.method == 'GET':
        form.project_title.data = update_task.project_title
        form.parent_id.data = update_task.parent_id      
        form.status.data = update_task.status
        form.task_description.data = update_task.task_description
        form.start_date.data = update_task.start_date
        form.end_date.data = update_task.end_date
        form.resource.data = update_task.resource_id      
    return render_template('tasks.html', title='Update Task', form=form )

@app.route("/tasks", methods=['GET', 'POST'])
def tasks(status='Not Started'):
    form = TaskForm()
    resource_id=request.form.get('resource')
    if form.validate_on_submit():
        flash(f'Resource {form.task_description.data} saved!', 'success')
        #task = Task(project_title=form.project_title.data, parent_id=form.parent_id.data, status=form.status.data, task_description=form.task_description.data, start_date=form.start_date.data, end_date=form.end_date.data, resource_id=form.resource.data)
        task = Task(project_title=form.project_title.data, parent_id=form.parent_id.data, status=request.form.get('status'), task_description=form.task_description.data, start_date=form.start_date.data, end_date=form.end_date.data, resource_id=request.form.get('resource'))
        db.session.add(task)
        db.session.commit()
    return render_template('tasks.html', title='Tasks', form=form )



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
        data_xls.to_sql(name='task', con=db.engine, if_exists='append',index=False)
    return render_template('upload.html', title='Upload Excel File')