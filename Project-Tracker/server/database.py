from flask_sqlalchemy import SQLAlchemy

# Create Flask-SQLAlchemy.
db = SQLAlchemy()


def initialize(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    db.session.commit()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Integer, db.ForeignKey('task_list.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.Text(200))
    date_completed = db.Column(db.DateTime)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assigned_to = db.Column(db.ForeignKey('user.cws'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.Text(200))
    date_created = db.Column(db.DateTime)


class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    activity = db.Column(db.String(20), nullable=False)
    task = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(120))
    estimated_hours = db.Column(db.Integer, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cws = db.Column(db.String(10), unique=True, nullable=False)
    psoft = db.Column(db.String(10))
    name = db.Column(db.String(40), nullable=False)
    supervisor_id = db.Column(db.ForeignKey('user.id'))
    reportees = db.relationship('User', foreign_keys=[supervisor_id])
    role = db.Column(db.String(10), default='')
    access = db.Column(db.String(10), default='user')
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    activities = db.relationship('Activity',
                                 backref=db.backref('owner'))
