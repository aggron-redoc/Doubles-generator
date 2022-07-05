from replit import db
from flask_restful import Resource
from Resources.args import groupReqArgs
from Resources.teams import Teams
from Resources.utilities import auth, dbUpdater

groupDeleteArgs = groupReqArgs.copy()
groupDeleteArgs.remove_argument('player')
playerDeleteArgs = groupReqArgs.copy()
groupClearArgs = groupReqArgs.copy()
groupClearArgs.remove_argument('player')
'''
patch method removes a player from the group after appropriate authentication and check if the player is in group

delete method deletes the group whose parameters have been passed in the request
'''


class GroupDelete(Resource):
    def patch(self):
        args = playerDeleteArgs.parse_args()
        if auth(args):
            if args['player'] not in db[args['groupId']]['participants']:
                return 'Player Not Found in Group', 400
            Team = Teams(list(db[args['groupId']]['participants']),
                         manipulate=list(db[args['groupId']]['manipulate']),
                         coupling=list(db[args['groupId']]['coupling']))
            Team.remove(args['player'])
            dbUpdater(Team, args)
            return 'Player ' + args['player'] + ' deleted successfully'
        else:
            return 'Group not found', 404

    def delete(self):
        args = groupDeleteArgs.parse_args()
        if auth(args):
            del db[args['groupId']]
            return 'Object Deleted Successfully'
        else:
            return 'Group not found', 404


'''
clear of this resource, clears all the previously formed teams. so already formed pairs are available again
'''


class GroupClear(Resource):
    def patch(self):
        args = groupClearArgs.parse_args()
        if auth(args):
            Team = Teams(list(db[args['groupId']]['participants']),
                         manipulate=list(db[args['groupId']]['manipulate']),
                         coupling=list(db[args['groupId']]['coupling']))
            Team.Clear()
            dbUpdater(Team, args)
            return 'Teams Cleared! All combinations available again!'
        else:
            return 'Group not found', 404
