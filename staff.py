from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ
from classes import *

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

db.init_app(app)

@app.route("/staff")
def get_all():
    stafflist = Staff.query.all()
    if len(stafflist):
        return jsonify(
            {
                "code":200,
                "data": {
                    "staff": [staff.json() for staff in stafflist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no staff."
        }
    ), 404

@app.route("/staff/<int:staff_id>")
def find_by_staff_id(staff_id):
    staff = Staff.query.get(staff_id)
    if staff:
        return jsonify(
            {
                "code": 200, 
                "staff": staff.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Staff not found."
        }
    ), 404
    
@app.route("/staff/skill/<int:skill_id>")
def find_by_skill(skill_id):
    staff = Skills.query.filter_by(skill_id=skill_id, ss_status='active')
    res= []
    for staffs in staff:
        res.append(Staff.query.get(staffs.staff_id).json())
    if len(res):
        return jsonify(
            {
                "code":200,
                "data": {
                    "staff": res
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no staff."
        }
    ), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)