from flask_restful import Resource


#Resource for root - uptime monitor pings it to keep the service alive
class PingClass(Resource):
    def get(self):
        return "Ping Successful!"
