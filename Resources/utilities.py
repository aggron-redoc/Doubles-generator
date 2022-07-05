from replit import db
import bcrypt
import json


#bcrypt for hashing password and checking if correct password was sent via hash
def auth(args):
    return args['groupId'] in db.keys() and (bcrypt.checkpw(
        bytes(args['password'], 'utf-8'),
        bytes(db[args['groupId']]['password'], 'utf-8')))


#Updating db with regards to team parameters on performing an action like randomize, add, remove etc
def dbUpdater(Team, args):
    participants = Team.participants[:]
    if ('pairing' in participants):
        participants.remove('pairing')
    db[args['groupId']]['participants'] = participants
    db[args['groupId']]['manipulate'] = Team.manipulate
    db[args['groupId']]['coupling'] = Team.coupling


#Returns hash for the passed string using bcrypt module
def hash(args):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(args['password'], 'utf-8'), salt)
    return hashed.decode('utf-8')


#Ensures newly created group's id is unique and returns True if not so
def postValidator(args):
    if (args['groupId'] in db.keys() or args['groupId'] == ''):
        return True


#returns all the data stored in database pertaining to group(password excluded)
def selectAll(args):
    response = {}
    response['players'] = list(db[args['groupId']]['participants'])
    response['manipulate'] = list(db[args['groupId']]['manipulate'])
    response['coupling'] = list(db[args['groupId']]['coupling'])
    return json.dumps(response)
