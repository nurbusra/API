from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
# this comment for ubuntu git test
#from busra

app = Flask(__name__)
api = Api(app)

class Courses(Resource):
    def get(self):
        data = pd.read_csv('courses.csv')
        data = data.to_dict('records')
        
        return {'data' : data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course_title')
        parser.add_argument('price')
        args = parser.parse_args()

        data = pd.read_csv('courses.csv')

        new_data = pd.DataFrame({
            'course_title'      : [args['course_title']],
            'price'      : [args['price']],
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('courses.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 201
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course_title', required=True)
        parser.add_argument('price', required=True)
        args = parser.parse_args()

        data = pd.read_csv('courses.csv')

        data = data[data['course_title'] != args['course_title']]

        data.to_csv('courses.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200

api.add_resource(Courses, "/courses")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
