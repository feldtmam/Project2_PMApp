import os
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import ResourcesForm, TaskForm, UpdateResourceForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pmappdb.db'

db = SQLAlchemy(app)

# to import the db - termnal -> from pmapp import db
class Resource(db.Model):
    resource_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False) 
    allocation_percentage = db.Column(db.Integer, nullable=False)
    marker_image = db.Column(db.String(20), nullable=False, default='default_marker.jpg')
    tasks = db.relationship('Task', backref='resource', lazy=True)


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.resource_id'), nullable=False)
    project_title = db.Column(db.String(150), nullable=False)
    parent_id = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(15), nullable=False)
    task_description = db.Column(db.String(200), nullable=False) 
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)



# dummy data
task=[]


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
    if form.validate_on_submit():
        if form.marker_image.data:
            marker_image_file = save_marker_image(form.marker_image.data)
        flash(f'Resource {form.fullname.data} saved!', 'success')
        resource = Resource(fullname=form.fullname.data, department=form.department.data, allocation_percentage=form.allocation_percentage.data, marker_image=marker_image_file)
        db.session.add(resource)
        db.session.commit()
    return render_template('resources.html', title='Resources', form=form) 

@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        flash(f'Resource {form.task_description.data} saved!', 'success')
        task = Task(project_title=form.project_title.data, parent_id=form.parent_id.data, status=form.status.data, task_description=form.task_description.data, start_date=form.start_date.data, end_date=form.end_date.data, resource_id=form.resource.data)
        db.session.add(task)
        db.session.commit()
    return render_template('tasks.html', title='Tasks', form=form ) #passing the dummy data to the web page - removed posts=task

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__': #use this to run the script in debug mode so we don't have to restart the server all the time
    app.run(debug=True)