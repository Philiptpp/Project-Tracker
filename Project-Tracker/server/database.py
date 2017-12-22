from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging


db = SQLAlchemy()
'''
# Database tables
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cws = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(40))
    role = db.Column(db.String(10))
    isactive = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(self, cws, name, role="user", isactive=True, date_created=datetime.utcnow(), date_modified=datetime.utcnow()):
        self.cws, self.name, self.role, self.isactive, self.date_created, self.date_modified = \
            cws, name, role, isactive, date_created, date_modified

    def __repr__(self):
        return '{:3}. {:40} [{:10}] @ {:10} (active: {}) created-on: {} [last-modified: {}]'.format(
            self.id, self.name, self.cws, self.role, self.isactive, self.date_created, self.date_modified)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.isactive

    def is_anonymous(self):
        if self.cws == 'guest':
            return True
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def create_user(cws, name, role='user'):
        try:
            user = User(cws=cws, name=name, role=role)
            db.session.add(user)
            db.session.commit()
            return {'message': 'New user created successfully', 'code': '200', 'data': str(user)}
        except Exception as e:
            return {'message': 'Failed to create new user', 'code': '404', 'data': str(e)}

    @staticmethod
    def delete_user(cws):
        try:
            user = User.query.filter(User.cws == cws).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User has been deleted', 'code': '200', 'data': str(user)}
            else:
                {'message': 'User not found', 'code': '404', 'data': str(e)}
        except Exception as e:
            return {'message': 'Unable to delete user', 'code': '404', 'data': str(e)}

    @staticmethod
    def update_user(cws, name, role, isactive):
        try:
            user = User.query.filter(User.cws == cws).first()
            if user:
                user.name, user.role, user.isactive, user.date_modified = name, role, isactive, datetime.utcnow()
                db.session.commit()
                return {'message': 'User info has been updated', 'code': '200', 'data': str(user)}
            else:
                {'message': 'User not found', 'code': '404', 'data': str(e)}
        except Exception as e:
            return {'message': 'Unable to update user info', 'code': '404', 'data': str(e)}


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(120))
    type = db.Column(db.String(20), nullable=False)
    sub_type = db.Column(db.String(20), nullable=False)
    activity = db.Column(db.String(20), nullable=False)
    sizeable = db.Column(db.Boolean)
    estimated_hours = db.Column(db.Integer)
    created_by = db.Column(db.ForeignKey('user.cws'))
    date_created = db.Column(db.DateTime)
    modified_by = db.Column(db.ForeignKey('user.cws'))
    date_modified = db.Column(db.DateTime)
    isactive = db.Column(db.Boolean)
    
    def __init__(self, description, type, sub_type, activity, estimated_hours, created_by, modified_by,
                 sizeable=False, isactive=True, date_created=datetime.utcnow(), date_modified=datetime.utcnow()):
        self.description, self.type, self.sub_type, self.activity, self.estimated_hours, \
        self.created_by, self.modified_by, self.sizeable, self.isactive, self.date_created, self.date_modified = \
            description, type, sub_type, activity, estimated_hours, created_by, modified_by, \
            sizeable, isactive, date_created, date_modified

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def create(description, type, sub_type, activity, estimated_hours, created_by, 
               sizeable=False, isactive=True, date_created=datetime.utcnow()):
        try:
            user = User.query.filter(User.cws == created_by).first()
            if not user:
                raise Exception("Unknown user")
            if not user.isactive:
                raise Exception("User '{}' is currently inactive".format(created_by.cws))
            activity = Activity(description=description, type=type, sub_type=sub_type, activity=activity,
                                estimated_hours=estimated_hours, created_by=created_by, modified_by=created_by,
                                sizeable=sizeable, isactive=isactive, date_created=date_created)
            db.session.add(activity)
            db.session.commit()
            return {'message': 'New activity created successfully', 'code': '200', 'data': str(activity)}
        except Exception as e:
            return {'message': 'Failed to create new activity', 'code': '404', 'data': str(e)}

    @staticmethod
    def delete(id):
        try:
            activity = Activity.query.get(id)
            if activity:
                activity.isactive = False
                db.session.commit()
                return {'message': 'Activity has been deleted', 'code': '200', 'data': str(activity)}
            else:
                {'message': 'Activity not found', 'code': '404', 'data': str(e)}
        except Exception as e:
            return {'message': 'Unable to delete activity', 'code': '404', 'data': str(e)}

    @staticmethod
    def update(id, description, type, sub_type, activity, estimated_hours, modified_by, 
               sizeable, isactive, date_modified=datetime.utcnow()):
        try:
            act = Activity.query.get(id)
            if act:
                user = User.query.filter(User.cws == modified_by).first()
                if not user:
                    raise Exception("Unknown user")
                if not user.isactive:
                    raise Exception("User '{}' is currently inactive".format(created_by.cws))
                act.description, act.type, act.sub_type, act.activity,
                act.estimated_hours, act.modified_by, act.sizeable, act.isactive, act.date_modified =\
                description, type, sub_type, activity, estimated_hours, modified_by, sizeable, isactive, date_modified
                db.session.commit()
                return {'message': 'Activity info has been updated', 'code': '200', 'data': str(act)}
            else:
                {'message': 'Activity not found', 'code': '404', 'data': str(e)}
        except Exception as e:
            return {'message': 'Unable to update activity info', 'code': '404', 'data': str(e)}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.Text(120))
    comments = db.Column(db.Text(500))
    facility = db.Column(db.String(20))
    activity = db.Column(db.ForeignKey('activity.id'))
    size = db.Column(db.String(10))
    estimated_hours = db.Column(db.Integer)
    received_date = db.Column(db.DateTime)
    target_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    created_by = db.Column(db.ForeignKey('user.cws'))
    date_created = db.Column(db.DateTime)
    modified_by = db.Column(db.ForeignKey('user.cws'))
    date_modified = db.Column(db.DateTime)
    user = db.Column(db.ForeignKey('user.cws'))
    """
    def __init__(self, name, description, comments, facility, activity, size, estimated_hours,
                 received_date, target_date, completed_date, status, created_by, date_created, date_modified):
        self.name, self.description, self.comments, self.facility, self.activity, self.size, self.estimated_hours, \
        self.received_date, self.target_date, self.completed_date, self.status, self.created_by, self.date_created, self.date_modified = \
            name, description, comments, facility, activity, size, estimated_hours, \
            received_date, target_date, completed_date, status, created_by, date_created, date_modified
    """
    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def update(name, description, facility, activity, size, estimated_hours, received_date,
               target_date, completed_date, status, user, comments,
               id=None):
        try:
            _user = User.query.filter(User.cws == user).first()
            if not _user:
                raise Exception("Unknown user")
            if not _user.isactive:
                raise Exception("User '{}' is currently inactive".format(_user.cws))
            
            task = Task.query.get(id)
            if not task:
                task = Task()
                task.created_by, task.date_created, task.user = user, datetime.utcnow(), user
                db.session.add(task)
            task.name = name
            task.description = description
            task.comments = comments
            task.facility = facility
            task.activity = activity
            task.size = size
            task.estimated_hours = estimated_hours
            task.received_date = received_date
            task.target_date = target_date
            task.completed_date = completed_date
            task.status = status
            task.modified_by = user
            task.date_modified = datetime.utcnow()
            db.session.commit()
            return {'message': 'Task updated successfully', 'code': '200', 'data': str(task)}
        except Exception as e:
            return {'message': 'Failed to update task', 'code': '404', 'data': str(e)}

    """
    @staticmethod
    def create(name, description, facility, activity, size, estimated_hours, received_date,
               target_date, completed_date, status, created_by, modified_by, comments,
               date_created=datetime.utcnow(), date_modified=datetime.utcnow()):
        try:
            user = User.query.filter(User.cws == created_by).first()
            if not user:
                raise Exception("Unknown user")
            if not user.isactive:
                raise Exception("User '{}' is currently inactive".format(created_by.cws))
            task = Task(name=name, description=description, facility=facility, activity=activity, size=size,
                        estimated_hours=estimated_hours, comments=comments, created_by=created_by, modified_by=modified_by,
                        received_date=received_date, target_date=target_date, completed_date=completed_date,
                        status=status, date_created=date_created, date_modified=date_modified)
            db.session.add(task)
            db.session.commit()
            return {'message': 'New task created successfully', 'code': '200', 'data': str(task)}
        except Exception as e:
            return {'message': 'Failed to create new task', 'code': '404', 'data': str(e)}
    """
    @staticmethod
    def delete(id):
        try:
            task = Task.query.get(id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return {'message': 'Task has been deleted', 'code': '200', 'data': str(task)}
            else:
                {'message': 'Task not found', 'code': '404', 'data': str(e)}
        except Exception as e:
            return {'message': 'Unable to delete task', 'code': '404', 'data': str(e)}
    """
    @staticmethod
    def update(id, name, description, facility, activity, size, estimated_hours, received_date,
               target_date, completed_date, status, modified_by, comments, date_modified=datetime.utcnow()):
        try:
            task = Task.query.get(id)
            if task:
                user = User.query.filter(User.cws == modified_by).first()
                if not user:
                    raise Exception("Unknown user")
                if not user.isactive:
                    raise Exception("User '{}' is currently inactive".format(created_by.cws))
                task.name, task.description, task.facility, task.activity, task.size, task.estimated_hours,
                task.comments, task.modified_by, task.received_date, task.target_date, task.completed_date,
                task.status, task.date_modified = \
                name, description, facility, activity, size, estimated_hours, comments, modified_by,
                received_date, target_date, completed_date, status, date_modified
                db.session.commit()
                return {'message': 'Task has been updated', 'code': '200', 'data': str(task)}
            else:
                {'message': 'Task not found', 'code': '404', 'data': str(e)}
        except Exception as e:
            return {'message': 'Unable to update task', 'code': '404', 'data': str(e)}
    """

'''
# Initialize database
'''
def init(app):
    try:
        app.app_context().push()
        db.init_app(app)
        db.create_all()
        db.session.commit()
        return True
    except:
        return False


def flush():
    db.drop_all()
    db.session.commit()
    return True


def format():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return True
