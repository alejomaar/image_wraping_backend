import functions_framework
import flask
from flask import jsonify
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    ValidationError,
    field_validator,
    validator,
)

@functions_framework.http
def main(request: flask.Request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    image_base64 = request_json.get("image_base64")

    response = {"ok": True, "data": image_base64}

    if not image_base64:
        return "Image does not exist", 400
    return jsonify(response), 200
