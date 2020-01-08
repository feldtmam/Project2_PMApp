from pmapp import db
from pmapp import db

db.Model.metadata.reflect(db.engine)

class Resource(db.Model):
    __tablename__ = 'resource'
    __table_args__ = { 'extend_existing' : True} # althrough sqlalchemy learned the table, we're telling it we're going to change it
    resource_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False) 
    allocation_percentage = db.Column(db.Integer, nullable=False)
    marker_image = db.Column(db.String(20), nullable=False, default='default_marker.jpg')
    tasks = db.relationship('Task', backref='resource', lazy=True)
    def __str__(self):
        return self.fullname

class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = { 'extend_existing' : True}
    task_id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.String, db.ForeignKey('resource.resource_id'), nullable=False)
    project_title = db.Column(db.String(150), nullable=False)
    parent_id = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(15), nullable=False)
    task_description = db.Column(db.String(200), nullable=False) 
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

