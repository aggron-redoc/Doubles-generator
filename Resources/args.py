from flask_restful import reqparse
'''
  The base requirement parser used for parsing data from requests in resources
'''

groupReqArgs = reqparse.RequestParser()
groupReqArgs.add_argument("groupId",
                          type=str,
                          location='headers',
                          required=True)
groupReqArgs.add_argument("password",
                          type=str,
                          location='headers',
                          required=True)
groupReqArgs.add_argument("player", type=str, required=True)
