from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ
from classes import *
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
            .join(Role_listing, Role_skill.role_id == Role_listing.role_id)
            .filter(Role_listing.role_listing_id == role_listing_id)
            .all()
        )
        staff_skills = (
            db.session.query(Skills.skill_id)
            .filter(Skills.staff_id == staff_id)
            .filter(Skills.ss_status == 'active')
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

@app.route('/skills/role/<int:role_id>')
def get_skills_by_role(role_id):
    try:
        skills = Role_skill.query.filter_by(role_id=role_id)
        return jsonify({
            "code": 200,
            "skills": [skill.json() for skill in skills]
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

@app.route('/role-skill')
def get_role_skills():
    try:
        role_skills = Role_skill.query.all()
        return jsonify({
            "code": 200,
            "skills": [role_skill.json() for role_skill in role_skills]
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)