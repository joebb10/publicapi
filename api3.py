import re

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def check_vulnerability(contract_code):
    # Check for the "unchecked-send" vulnerability
    pattern = r"call.value\((.+)\)"
    match = re.search(pattern, contract_code)
    if match:
        unchecked_send = "Vulnerability found: unchecked-send"
    else:
        unchecked_send = "No unchecked-send vulnerability found."

    # Check for the "uninitialized-storage-pointer" vulnerability
    pattern = r"storage\[(.+)\] ="
    match = re.search(pattern, contract_code)
    if match:
        storage = "Vulnerability found: uninitialized-storage-pointer"
    else:
        storage = "No uninitialized-storage-pointer vulnerability found."

   

@app.route('/check_vulnerability', methods=['POST'])
def check_vuln():
    content = request.get_json()

    if 'contract_code' in content:
        contract_code = content['contract_code']
        results = check_vulnerability(str(contract_code))
        return jsonify({"unchecked_send": results[0], 
                        "uninitialized_storage_pointer": results[1],
                        })
    return jsonify("You didn't send contract code on body..")
if __name__ == '__main__':
    app.run(debug=True)
