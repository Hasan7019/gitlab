from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ
from classes import *
import requests

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

@app.route("/staff/email/<string:email>")
def find_by_email(email):
    staff = Staff.query.filter_by(email=email).first()
    if staff:
        return jsonify({
            "code": 200,
            "staff": staff.json()
        }), 200
    return jsonify({
        "code": 404,
        "message": "Staff not found."
    }), 404


@app.route("/staff/skill")
def get_staff_skills():
    try: 
        staff = Skills.query.filter_by(ss_status = 'active').all()
        res = [data.json() for data in staff]
        return jsonify({
            "code": 200,
            "data": res
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"an unexcepted error occured {str(e)}"
        }), 500
    
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

@app.route("/staff/suitable/<int:role_id>")
def find_suitable_candidates(role_id):
    try:
        skills_needed = requests.get(f"http://skill:5001/skills/role/{role_id}").json()['skills']
        skills = requests.get("http://staff:5000/staff/skill").json()['data']
        suitable = {}
        for needed in skills_needed:
            for staff in skills:
                if needed['skill_id'] == staff['skill_id']:
                    if staff['staff_id'] not in suitable:
                        suitable[staff['staff_id']] = 1
                    else:
                        suitable[staff['staff_id']] += 1
        temp = []
        for staff_id in suitable:
            temp.append((staff_id, suitable[staff_id]))
        sorted_temp = sorted(temp, key=lambda x:x[1])
        staffs = requests.get("http://staff:5000/staff").json()['data']['staff']
        res = []
        for i in sorted_temp:
            for staff in staffs:
                if staff['staff_id'] == i[0]:
                    staff['matches'] = i[1]
                    if i[1] == len(skills_needed):
                        staff['match'] = True
                    else:
                        staff['match'] = False
                    res.append(staff)
        return jsonify({
                "code": 200,
                "data": res
            })
            
    except Exception as e:
            return jsonify({
                "code": 500,
                "error": "An unexpected error occurred: " + str(e)
            }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)