import pymongo
from flask  import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import json, datetime

url = "mongodb://namwan:namwan3439@localhost:27017/admin"
client = pymongo.MongoClient(url)

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('information')

db=client.admin.cpe_company_limited
listwork = []
st = []
class Registration(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['information'])
		db.insert(      {"id":data['id'],
				"firstname":data['firstname'],
				"lastname":data['lastname'],
				"password":data['password']})
		return{'firstname':data['firstname']}


class Login(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['information'])
		result = db.find({'id': data['id']})
		today = datetime.datetime.today()
		now = today.strftime('%Y-%m-%d %H:%M:%S')
		listwork.append(str(now))
		db.update({"id":data['id']},
			{'$set':
			{'list_work': listwork}})
		print result,">>",len(listwork)
		return {'firstname': result['firstname'], 'datetime': now}

class History(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['information'])
		result = db.find({'id': data['id']})
		print result
		print ">>>>>>>>><<<<<<<<<<<<<<<<<"
		return {'id': result['id'], 'firstname': result['firstname'], 'list_work': result['list_work']}

api.add_resource(Registration,'/Registration')
api.add_resource(Login,'/Login')
api.add_resource(History,'/History')


if __name__=='__main__':
	app.run(host='0.0.0.0',port=5001, debug=True)





