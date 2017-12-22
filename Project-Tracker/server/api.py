from flask_restful import Api, Resource, reqparse
import database


class Users(Resource):
    parser = reqparse.RequestParser()
    def __init__(self):
        Users.parser.add_argument('cws', type=str, required=True, help="CWS id for the user [must be unique]")
        Users.parser.add_argument('name', type=str, required=True, help="Full name as should be displayed")
        Users.parser.add_argument('role', type=str, help="Role [user, admin, guest]")
        Users.parser.add_argument('is_active', type=bool, help="Is the account currently active")
    def get(self):
        return [str(user) for user in database.User.query.all()]
    def post(self):
        data = Users.parser.parse_args()
        return database.User.create_user(cws=data.cws, name=data.name, role=data.role)
    def delete(self):
        data = Users.parser.parse_args()
        return database.User.delete_user(cws=data.cws)
    def put(self):
        data = Users.parser.parse_args()
        return database.User.update_user(cws=data.cws, name=data.name, role=data.role, isactive=data.is_active)


class Activities(Resource):
    parser = reqparse.RequestParser()
    def __init__(self):
        Activities.parser.add_argument('id', type=int)
        Activities.parser.add_argument('description', type=str)
        Activities.parser.add_argument('type', type=str)
        Activities.parser.add_argument('sub_type', type=str)
        Activities.parser.add_argument('activity', type=str)
        Activities.parser.add_argument('sizeable', type=bool)
        Activities.parser.add_argument('estimated_hours', type=int)
        Activities.parser.add_argument('user', type=str, required=True)
        Activities.parser.add_argument('isactive', type=bool)
    def get(self):
        return [str(activity) for activity in database.Activity.query.all() if activity.isactive == True]
    def post(self):
        data = Activities.parser.parse_args()
        return database.Activity.create(description=data.description, type=data.type, sub_type=data.sub_type,
                                        activity=data.activity, estimated_hours=data.estimated_hours, created_by=data.user,
                                        sizeable=data.sizeable)
    def delete(self):
        data = Activities.parser.parse_args()
        return database.Activity.delete(id=data.id)
    def put(self):
        data = Activities.parser.parse_args()
        return database.Activity.update(id=data.id, description=data.description, type=data.type, sub_type=data.sub_type,
                                        activity=data.activity, estimated_hours=data.estimated_hours, modified_by=data.user, 
                                        sizeable=data.sizeable, isactive=data.isactive)


class Tasks(Resource):
    parser = reqparse.RequestParser()
    def __init__(self):
        Tasks.parser.add_argument('id', type=int)
        Tasks.parser.add_argument('name', type=str)
        Tasks.parser.add_argument('description', type=str)
        Tasks.parser.add_argument('facility', type=str)
        Tasks.parser.add_argument('activity', type=int)
        Tasks.parser.add_argument('size', type=str)
        Tasks.parser.add_argument('estimated_hours', type=int)
        Tasks.parser.add_argument('received_date', type=str)
        Tasks.parser.add_argument('target_date', type=str)
        Tasks.parser.add_argument('completed_date', type=str)
        Tasks.parser.add_argument('status', type=str)
        Tasks.parser.add_argument('comments', type=str)
        Tasks.parser.add_argument('user', type=str, required=True)
    def get(self):
        data = Tasks.parser.parse_args()
        return [str(task) for task in database.Task.query.all() if task.user == data.user]
    def post(self):
        data = Tasks.parser.parse_args()
        print(data)
        return database.Task.update(name=data.name, description=data.description, facility=data.facility,
                                    activity=data.activity, size=data.size, estimated_hours=data.estimated_hours, 
                                    received_date=data.received_date, target_date=data.target_date,
                                    completed_date=data.completed_date, status=data.status, comments=data.comments,
                                    user=data.user)
    def delete(self):
        data = Tasks.parser.parse_args()
        return database.Task.delete(id=data.id)
    def put(self):
        data = Tasks.parser.parse_args()
        return database.Task.update(name=data.name, description=data.description, facility=data.facility,
                                    activity=data.activity, size=data.size, estimated_hours=data.estimated_hours, 
                                    received_date=data.received_date, target_date=data.target_date,
                                    completed_date=data.completed_date, status=data.status, comments=data.comments,
                                    user=data.user, id=data.id)


def init(app):
    api.init_app(app)
    database.init(app)


api = Api(None, '/api/v1')
api.add_resource(Users, '/users')
api.add_resource(Activities, '/activities')
api.add_resource(Tasks, '/tasks')
