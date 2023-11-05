from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ
from classes import *

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/roles')
def get_all():
    roleList = Role.query.all()
    if len(roleList):
        return jsonify({
            "code": 200,
            "data": {
                "role": [role.json() for role in roleList]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no roles"
    }), 404

@app.route('/roles', methods=["POST"])
def add_role():
    try:
        data = request.get_json()

        new_role = Role(
            role_id=data["role_id"],
            role_name=data["role_name"],
            role_description=data["role_description"],
            role_status=data["role_status"]
        )
        db.session.add(new_role)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Role added successfully",
            "role": new_role.json()
        }), 201

    except KeyError as e:
        return jsonify({
            "code": 400,
            "error": "Missing or invalid key in the request body: " + str(e)
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

@app.route('/roles/<int:role_id>')
def find_by_role_id(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if role:
        return jsonify({
            "code": 200,
            "role": role.json()
        }), 200
    return jsonify({
        "code": 404,
        "message": "Role not found."
    }), 404

@app.route('/role-listings')
def get_all_listings():
    listingList = Role_listing.query.all()
    if len(listingList):
        return jsonify({
            "code": 200,
            "data": {
                "listing": [listing.json() for listing in listingList]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no role listings."
    }), 404

@app.route('/role-listings/<int:role_listing_id>')
def get_listing(role_listing_id):
    listing = Role_listing.query.get(role_listing_id)
    if listing:
        return jsonify({
            "code": 200,
            "listing": listing.json()
        }), 200
    return jsonify({
        "code": 404,
        "message": "Role listing not found."
    }), 404

@app.route("/role-listings/<int:role_listing_id>", methods=["PUT"])
def update_role_listing(role_listing_id):
    try:
        data = request.get_json()
        existing_role_listing = Role_listing.query.get(role_listing_id)

        if not existing_role_listing:
            return jsonify({
                "code": 404,
                "error": "Role listing not found"
            }), 404

        for key, value in data.items():
            setattr(existing_role_listing, key, value)

        db.session.commit()

        return jsonify({
            "code": 200,
            "message": "Role listing updated successfully", 
            "role_listing": existing_role_listing.json()
        }), 200

    except KeyError as e:
        return jsonify({
            "code": 400,
            "error": "Missing or invalid key in the request body: " + str(e)
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

@app.route('/role-listings', methods=["POST"])
def add_role_listing():
    try:
        data = request.get_json()
        new_role_listing = Role_listing(
            role_listing_id=data["role_listing_id"],
            role_id=data["role_id"],
            role_listing_desc=data["role_listing_desc"],
            role_listing_source=data["role_listing_source"],
            role_listing_open=data["role_listing_open"],
            role_listing_close=data.get("role_listing_close"),  # Optional field
            role_listing_creator=data["role_listing_creator"],
            role_listing_ts_create=data["role_listing_ts_create"],
            role_listing_updater=data["role_listing_updater"],
            role_listing_ts_update=data["role_listing_ts_update"],
        )
        db.session.add(new_role_listing)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Role listing added successfully",
            "role_listing": new_role_listing.json()
        }), 201
    except KeyError as e:
        return jsonify({
            "code": 400,
            "error": "Missing or invalid key in the request body: " + str(e)
        }), 400
    except IntegrityError as e: 
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "Database error: " + str(e)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "An unexpected error occured: " + str(e)
        }), 500
    
@app.route('/filter-role-listings-by-skills', methods=["GET"])
def filter_role_listings_by_skills():
    try:
        skill_ids_param = request.args.get("skill_ids")

        if not skill_ids_param:
            return jsonify({
                "code": 400,
                "error": "No skill_ids provided in query parameters"
            }), 400

        skill_ids = [int(skill_id) for skill_id in skill_ids_param.split(",")]

        filtered_role_listings = (
            db.session.query(Role_listing)
            .join(Role_skill, Role_listing.role_id == Role_skill.role_id)
            .filter(Role_skill.skill_id.in_(skill_ids))
            .distinct()
            .all()
        )
        db.session.close()

        filtered_role_listings_json = [listing.json() for listing in filtered_role_listings]

        return jsonify({
            "code": 200,
            "filtered_role_listings": filtered_role_listings_json
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

@app.route('/role-applications')
def get_applications():
    applicationList = Role_application.query.all()
    if len(applicationList):
        return jsonify({
            "code": 200,
            "data": {
                "application": [application.json() for application in applicationList]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no roles"
    }), 404

@app.route('/role-applications', methods=["POST"])
def create_role_application():
    try:
        data = request.get_json()

        new_role_application = Role_application(
            role_app_id=data["role_app_id"],
            role_listing_id=data["role_listing_id"],
            staff_id=data["staff_id"],
            role_app_status=data["role_app_status"],
            role_app_ts_create=data["role_app_ts_create"]
        )
        db.session.add(new_role_application)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Role application added successfully",
            "role_application": new_role_application.json()
        }), 201

    except KeyError as e:
        return jsonify({
            "code": 400,
            "error": "Missing or invalid key in the request body: " + str(e)
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

@app.route('/role-applications/<int:role_listing_id>/<int:staff_id>', methods=["GET"])
def find_role_application(role_listing_id, staff_id):
    role_application = Role_application.query.filter_by(role_listing_id=role_listing_id, staff_id=staff_id).first()

    if not role_application:
        return jsonify({
            "code": 404,
            "message": "No application found."
        }), 404
    
    return jsonify({
        "code": 200,
        "role_application": role_application.json()
    }), 200

@app.route('/role-applications/listing/<int:role_listing_id>', methods=["GET"])
def find_application_by_listing(role_listing_id):
    role_applications = Role_application.query.filter_by(role_listing_id=role_listing_id)

    if not role_applications:
        return jsonify({
            "code": 404,
            "message": "No applications found."
        }), 404
    
    return jsonify({
        "code": 200,
        "role_applications": [application.json() for application in role_applications]
    }), 200

@app.route("/role-applications/<int:role_app_id>", methods=["PUT"])
def update_role_application(role_app_id):
    try:
        data = request.get_json()
        existing_role_application = Role_application.query.get(role_app_id)

        if not existing_role_application:
            return jsonify({
                "code": 404,
                "error": "Role application not found"
            }), 404

        for key, value in data.items():
            setattr(existing_role_application, key, value)

        db.session.commit()

        return jsonify({
            "code": 200,
            "message": "Role listing updated successfully", 
            "role_listing": existing_role_application.json()
        }), 200

    except KeyError as e:
        return jsonify({
            "code": 400,
            "error": "Missing or invalid key in the request body: " + str(e)
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred: " + str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)