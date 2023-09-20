from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Staff(db.Model):
    __tablename__ = 'STAFF_DETAILS'

    staff_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.Integer)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    biz_address = db.Column(db.String(255))
    sys_role = db.Column(db.String(15))

    def __init__(self, staff_id, fname, lname, dept, email, phone, biz_address, sys_role):
        self.staff_id = staff_id
        self.fname = fname
        self.lname = lname
        self.dept = dept
        self.email = email
        self.phone = phone
        self.biz_address = biz_address
        self.sys_role = sys_role

    def json(self):
        return {"staff_id": self.staff_id, "fname": self.fname, "lname":self.lname, "dept": self.dept, "email": self.email, "phone": self.phone, "biz_address": self.biz_address, "sys_role": self.sys_role}

@app.route("/staff")
def get_all():
    staff = Staff.query.all()
    if len(stafft):
        return jsonify(
            {
                "code":200,
                "data": {
                    "staff": [book.json() for book in booklist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no staff."
        }
    ), 404

@app.route("/staff/<string:staff_id>")
def find_by_staff_id(staff_id):
    staff = Staff.query.filter_by(staff_id=staff_id).first()
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
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    


