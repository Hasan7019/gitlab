from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ

from role import Role_skill
from staff import Skills
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Skill(db.Model):
    __tablename__ = 'SKILL_DETAILS'

    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), nullable=False)
    skill_status = db.Column(Enum('active', 'inactive'), nullable=False)

    def __init__(self, skill_id, skill_name, skill_status):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_status = skill_status

    def json(self):
        return {"skill_id": self.skill_id, "skill_name": self.skill_name, "skill_status": self.skill_status}

@app.route('/skills')
def get_all():
    skillsList = Skill.query.all()
    if len(skillsList):
        return jsonify({
            "code": 200,
            "data": {
                "skill": [skill.json() for skill in skillsList]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no skills"
    }), 404

@app.route('/skills/<int:skill_id>')
def find_by_skill_id(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        return jsonify({
            "code": 200,
            "skill": skill.json()
        }), 200
    return jsonify({
        "code": 404,
        "message": "Skill not found."
    }), 404

@app.route('/get-lacking-skills/<int:staff_id>/<int:role_listing_id>')
def get_lacking_skills(staff_id, role_listing_id):
    try:
        if not staff_id or not role_listing_id:
            return jsonify({
                "code": 400,
                "error": "Missing staff_id or role_listing_id in query parameters"
            }), 400
        
        required_skills = (
            db.session.query(Role_skill.skill_id)
            .filter(Role_skill.role_id == role_listing_id)
            .all()
        )
        staff_skills = (
            db.session.query(Skills.skill_id)
            .filter(Skills.staff_id == staff_id)
            .all()
        )

        required_skills_set = set(skill[0] for skill in required_skills)
        staff_skills_set = set(skill[0] for skill in staff_skills)
        lacking_skill_ids = list(required_skills_set - staff_skills_set)
        lacking_skills = (
            db.session.query(Skill)
            .filter(Skill.skill_id.in_(lacking_skill_ids))
            .all()
        )

        return jsonify({
            "code":200,
            "lacking_skills": [skill.json() for skill in lacking_skills]
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)