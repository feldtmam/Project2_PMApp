from flask import Flask, render_template, url_for, flash, redirect
from forms import ResourcesForm, TaskForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# dummy data
task = [
    {
        'project_title': 'Test Project',
        'task_id': 1,
        'status': 'In Progress',
        'task_description': 'Requirements Definition (Phase 1)',
        'start_date': '11/30/2019',
        'end_date': '03/31/2020',
        'resource': 'Martie Feldtmann'
    },
    {
        'project_title': 'Test Project',
        'task_id': 1.01,
        'status': 'In Progress',
        'task_description': 'Requirements funding',
        'start_date': '12/01/2019',
        'end_date': '12/31/2019',
        'resource': 'Bob Iger'
    },
    {
        'project_title': 'Test Project',
        'task_id': 1.0101,
        'status': 'In Progress',
        'task_description': 'Review project request',
        'start_date': '12/01/2019',
        'end_date': '12/31/2019',
        'resource': 'Bob Iger'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/resources", methods=['GET', 'POST'])
def resources():
    form = ResourcesForm()
    if form.validate_on_submit():
        flash(f'Resource {form.fullname.data} saved!', 'success')
    return render_template('resources.html', title='Resources', form=form) 

@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        flash(f'Resource {form.task_description.data} saved!', 'success')
    return render_template('tasks.html', title='Tasks', form=form, posts=task) #passing the dummy data to the web page

@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__': #use this to run the script in debug mode so we don't have to restart the server all the time
    app.run(debug=True)