#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        response_dict = {"index": "Welcome to the Newsletter RESTful API"}
        return jsonify(response_dict), 200

api.add_resource(Index, '/')

class Newsletters(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        response_dict_list = [n.to_dict() for n in newsletters]
        return jsonify(response_dict_list), 200

    def post(self):
        title = request.form.get('title')
        body = request.form.get('body')

        new_record = Newsletter(title=title, body=body)
        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()
        return jsonify(response_dict), 201

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.get(id)

        if not newsletter:
            return make_response(jsonify({"error": "Newsletter not found"}), 404)

        response_dict = newsletter.to_dict()
        return jsonify(response_dict), 200

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)