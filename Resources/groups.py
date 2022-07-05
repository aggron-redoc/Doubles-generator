from replit import db
from flask_restful import Resource
from Resources.args import groupReqArgs
from Resources import utilities
from Resources.teams import Teams
import json

groupAddArgs = groupReqArgs.copy()
groupAddArgs.remove_argument('player')
groupAddArgs.add_argument('players', required=True, type=list, location='json')

groupAddGuyArgs = groupReqArgs.copy()

seeSoFarArgs = groupReqArgs.copy()
seeSoFarArgs.remove_argument('player')

randomizeArgs = groupReqArgs.copy()
randomizeArgs.remove_argument('player')
'''
patch method of groups - randomize and spits out the combinations if available
combinations provided and data updated by the class teams and result extracted from it
'''
'''
get method of groups - send the current status of group, who has teamed with whom so far.
'''


class Groups(Resource):
    def patch(self):
        args = randomizeArgs.parse_args()
        if (utilities.auth(args)):
            Team = Teams(list(db[args['groupId']]['participants']),
                         manipulate=list(db[args['groupId']]['manipulate']),
                         coupling=list(db[args['groupId']]['coupling']))
            response = Team.randomizer()
            utilities.dbUpdater(Team, args)
            return json.dumps(response)
        else:
            return 'Group not found', 404

    def get(self):
        args = seeSoFarArgs.parse_args()
        if (utilities.auth(args)):
            return utilities.selectAll(args)
        else:
            return 'Group not found', 404


'''
post for creating a new group
patch for adding a new player into the group. Adding and the required changes to the adjacency matrix made by teams class
'''


class GroupAdd(Resource):
    def post(self):
        args = groupAddArgs.parse_args()
        if (utilities.postValidator(args)):
            return 'GroupId Already exists', 409
        document = {}
        document['password'] = utilities.hash(args)
        db[args['groupId']] = document
        Team = Teams(args['players'])
        utilities.dbUpdater(Team, args)
        return 'New Group added to database'

    def patch(self):
        args = groupAddGuyArgs.parse_args()
        if utilities.auth(args):
            Team = Teams(list(db[args['groupId']]['participants']),
                         manipulate=list(db[args['groupId']]['manipulate']),
                         coupling=list(db[args['groupId']]['coupling']))
            Team.add(args['player'])
            utilities.dbUpdater(Team, args)
            return 'Player ' + args['player'] + ' added successfully'
        else:
            return 'Group not found', 404
