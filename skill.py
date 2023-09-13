# {
#     skillId1: {
#         skillName1: name,
#         employees: [
#             empId1,
#             empId2,
#             empId3
#         ]
#     },
#     skillId2: {
#         skillName2: name,
#         employees: [
#             empId1,
#             empId2,
#             empId3
#         ]
#     }
# }

from flask import Flask, request, jsonify, render_template, send_from_directory
import firebase_admin
from firebase_admin import firestore, credentials, initialize_app

app = Flask(__name__)

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/skills', methods=['POST'])
def add_skill():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Please provide data for the new skill'}), 400
    
    doc_ref = db.collection('skills').document()
    doc_ref.set(data)
    return jsonify({'message': 'Skill successfully added', 'id': doc_ref.id}), 201

@app.route('/skills/<string:skillId>', methods=['DELETE'])
def delete_skill(skillId):
    doc_ref = db.collection('skills').document(skillId)
    if not doc_ref.get().exists:
        return jsonify({'error': 'Skill not found.'}), 404
    doc_ref.delete()
    return jsonify({'message': 'Skill deleted successfully'}), 200

@app.route('/skills/<string:skillId>', methods=['PUT'])
def update_skill(skillId):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Please provide data to update the skill.'}), 400
    doc_ref = db.collection('skills').document(skillId)
    if not doc_ref.get().exists:
        return jsonify({'error': 'Skill not found.'}), 404
    doc_ref.update(data)
    return jsonify({'message': 'Skill updated successfully'}), 200

# @app.route('/skills', methods=['POST'])
# def add_skill_employee():
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'Please provide data for the new employee.'}), 400

#     doc_ref = db.collection('skills').document()
#     doc_ref.set(data)
#     return jsonify({'message': 'Employee successfully added', 'id': doc_ref.id}), 201

# @app.route('/skills/<string:employeeId>', methods=['GET'])
# def read_employee(employeeId):
#     doc_ref = db.collections('skills').document(employeeId)
#     doc = doc_ref.get()
#     if not doc.exists:
#         return jsonify({'error': 'Item not found'}), 404
#     return jsonify(doc.to_dict()), 200

# @app.route('/skills', methods=['GET'])
# def get_skills():
#     docs = db.collection('skills').get()
    
#     data = []
#     for doc in docs:
#         toAppend = doc.to_dict()
#         toAppend['id'] = doc.id
#         data.append(toAppend)
#     return jsonify(data), 200

# @app.route('/skills/<string:employeeId>', methods=['PUT'])
# def update_employee(employeeId):
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'Please provide data to update the bakery.'}), 400
#     doc_ref = db.collection('skills').document(employeeId)
#     if not doc_ref.get().exists:
#         return jsonify({'error': 'Listing not found.'}), 404
#     doc_ref.update(data)
#     return jsonify({'message': 'Listing updated successfully'}), 200

# @app.route('/skills/<string:employeeId>', methods=['DELETE'])
# def delete_employee(employeeId):
#     doc_ref = db.collection('skills').document(employeeId)
#     if not doc_ref.get().exists:
#         return jsonify({'error': 'Listing not found.'}), 404
#     doc_ref.delete()
#     return jsonify({'message': 'Listing deleted successfully'}), 200

# if __name__ == '__main__':
#     app.run(debug=True)