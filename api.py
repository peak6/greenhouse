from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from flask.ext.restful import Api, Resource

import ConfigParser
import json
import sys, traceback
import urllib2, base64

whitelist = ('127.0.0.1')

config = ConfigParser.RawConfigParser()
config.read("/etc/config/greenhouse.conf")

API_KEY = config.get('default', 'API_KEY')
API_URL = config.get('default', 'API_URL')
API_PROFESSIONAL_JOB_BOARD_URL = config.get('default', 'API_PROFESSIONAL_JOB_BOARD_URL')
API_STUDENT_JOB_BOARD_URL = config.get('default', 'API_STUDENT_JOB_BOARD_URL')

app = Flask(__name__)
CORS(app)

api = Api(app)


class CandidatesResource( Resource ):
	def get ( self ):
		request = urllib2.Request('%s/%s' % (API_URL, 'candidates'))

		# You need the replace to handle encodestring adding a trailing newline 
		# (https://docs.python.org/2/library/base64.html#base64.encodestring)
		base64string = base64.encodestring('%s:%s' % (API_KEY, '')).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)   
		response = urllib2.urlopen(request)

		return json.loads(response.read())		

class ProfessionalJobBoardResource( Resource ):
	def get ( self ):
		request = urllib2.Request(API_PROFESSIONAL_JOB_BOARD_URL)

		response = urllib2.urlopen(request)

		return json.loads(response.read())

class StudentJobBoardResource( Resource ):
	def get ( self ):
		request = urllib2.Request(API_PROFESSIONAL_JOB_BOARD_URL)

		response = urllib2.urlopen(request)

		return json.loads(response.read())


api.add_resource(CandidatesResource, '/candidates')
api.add_resource(ProfessionalJobBoardResource, '/jobs/professional')
api.add_resource(StudentJobBoardResource, '/jobs/student')


#	start the app
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=10002, debug=True, threaded=True)