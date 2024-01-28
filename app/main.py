import functions_framework
import flask
from flask import jsonify, send_file
import cv2
import numpy as np
import requests
from io import BytesIO


def read_image_from_url(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Convert the response content to a NumPy array
    image_array = np.frombuffer(response.content, dtype=np.uint8)

    # Decode the NumPy array to an OpenCV image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # If needed, convert color from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


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
    image_url = request_json.get("url")

    if not image_url:
        return "Image does not exist", 400

    opencv_img = read_image_from_url(image_url)

    is_ok, buffer = cv2.imencode(".jpg", opencv_img)
    if not is_ok:
        return "Error converting image to JPEG format", 500

    # Convert buffer to a byte stream
    byte_io = BytesIO(buffer)

    # Send the byte stream as a response
    return send_file(byte_io, mimetype="image/jpeg")
