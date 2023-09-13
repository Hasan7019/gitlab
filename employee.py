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

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Please provide data for the new employee.'}), 400

    doc_ref = db.collection('employees').document()
    doc_ref.set(data)
    return jsonify({'message': 'Employee successfully added', 'id': doc_ref.id}), 201

@app.route('/employees/<string:employeeId>', methods=['GET'])
def read_employee(employeeId):
    doc_ref = db.collections('employees').document(employeeId)
    doc = doc_ref.get()
    if not doc.exists:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(doc.to_dict()), 200

@app.route('/employees', methods=['GET'])
def get_employees():
    docs = db.collection('employees').get()
    
    data = []
    for doc in docs:
        toAppend = doc.to_dict()
        toAppend['id'] = doc.id
        data.append(toAppend)
    return jsonify(data), 200

@app.route('/employees/<string:employeeId>', methods=['PUT'])
def update_employee(employeeId):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Please provide data to update the bakery.'}), 400
    doc_ref = db.collection('employees').document(employeeId)
    if not doc_ref.get().exists:
        return jsonify({'error': 'Listing not found.'}), 404
    doc_ref.update(data)
    return jsonify({'message': 'Listing updated successfully'}), 200

@app.route('/employees/<string:employeeId>', methods=['DELETE'])
def delete_employee(employeeId):
    doc_ref = db.collection('employees').document(employeeId)
    if not doc_ref.get().exists:
        return jsonify({'error': 'Listing not found.'}), 404
    doc_ref.delete()
    return jsonify({'message': 'Listing deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)