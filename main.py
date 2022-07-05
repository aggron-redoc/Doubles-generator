from flask import Flask
from flask_restful import Api
from Resources.groups import Groups, GroupAdd
from Resources.group_delete import GroupDelete, GroupClear
from Resources.pingClass import PingClass
# from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
# CORS(app)

#Endpoints
api.add_resource(PingClass, "/")
api.add_resource(Groups, "/randomize")
api.add_resource(GroupAdd, "/add")
api.add_resource(GroupDelete, "/remove")
api.add_resource(GroupClear, "/clearAllTeams")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
