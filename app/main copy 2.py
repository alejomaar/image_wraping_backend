import numpy as np
import functions_framework
from flask import jsonify



@functions_framework.http
def main(request: dict):
    """HTTP Cloud Function for POST requests.
    Args:
        request (flask.Request): The request object.
    """
    # Assume the event dictionary has the base64 string under a key 'image'

    if request.method != "POST":
        return "This function only accepts POST requests.", 405

    request_json = request.get_json(silent=True)

    if request_json and "name" in request_json:
        data = request.get_json()
        base64_image = data["image"]
        print(base64_image)
        return base64_image

    else:
        return jsonify({"error": "Missing 'name' in request"}), 400
