from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

TENANT_ID = os.getenv("TENANT_ID")
CENTRAL_API = os.getenv("CENTRAL_API")

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/leadership' , methods=['GET'])
def get_leadership():
    year = request.args.get('year')
    if not year:
        return jsonify({"error": "Year parameter is required"}), 400
    
    res = requests.get(f"{CENTRAL_API}/api/v1/tenant/{TENANT_ID}/leaders")
    if res.ok:
        
        data = res.json()
        if str(year) in data:
            return jsonify(data[str(year)]), 200
    return jsonify({}),500

@app.route('/leadership', methods=['POST'])
def add_leadership():
    data = request.json
    year = data.get('year')
    if not year:
        return jsonify({"error": "Year is required"}), 400
    
    # Fetch existing leaders to avoid overwriting other years
    res = requests.get(f"{CENTRAL_API}/api/v1/tenant/{TENANT_ID}/leaders")
    leaders_data = res.json() if res.ok and res.json() else {}
    
    leaders_data[str(year)] = data
    
    post_res = requests.post(f"{CENTRAL_API}/api/v1/tenant/{TENANT_ID}/leaders", json=leaders_data)
    if post_res.ok:
        return jsonify({"message": "Leadership data updated successfully"}), 201
    return jsonify({"error": "Failed to update central API"}), 500

@app.route('/events', methods=['POST'])
def add_event():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    required_fields = ['eventname', 'eventdate', 'eventlocation']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Fetch existing
    res = requests.get(f"{CENTRAL_API}/api/v1/tenant/{TENANT_ID}/events")
    events_data = res.json() if res.ok and res.json() else {}
    
    # Convert list to dict if needed (since DB schema defines it as a dict)
    if isinstance(events_data, list):
        events_dict = {}
        for ev in events_data:
            events_dict[ev.get("eventname", "unknown").lower().replace(" ", "")] = ev
        events_data = events_dict

    key = data["eventname"].lower().replace(' ', '')
    events_data[key] = data

    post_res = requests.post(f"{CENTRAL_API}/api/v1/tenant/{TENANT_ID}/events", json=events_data)
    if post_res.ok:
        return jsonify({"message": "Event added successfully"}), 201
    return jsonify({"error": "Failed to add event to central API"}), 500

@app.route('/events', methods=['GET'])
def get_events():
    res = requests.get(f"{CENTRAL_API}/api/v1/tenant/{TENANT_ID}/events")
    if res.ok:
        events = res.json()
        # Convert dict back to list for frontend
        if isinstance(events, dict):
            events = list(events.values())
        return jsonify(events), 200
    return jsonify([]), 200

if __name__ == '__main__':
    app.run(debug=True)
