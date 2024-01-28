import flask
from flask import send_file
import cv2
import numpy as np
import requests
from io import BytesIO
import functions_framework


def read_image_from_url(url: str) -> np.ndarray:
    """
    Reads an image from a given URL.

    Args:
    - url (str): URL of the image to be downloaded.

    Returns:
    - np.ndarray: The image as a NumPy array.
    """
    response = requests.get(url)
    response.raise_for_status()
    image_array = np.frombuffer(response.content, dtype=np.uint8)
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

def warp_image(image: np.ndarray, src_points: np.ndarray, w: int, h: int) -> np.ndarray:
    """
    Warps an image from src_points to a new dimension (w, h).

    Args:
    - image (np.ndarray): Input image.
    - src_points (np.ndarray): Array of four source points in the order 
                               top-left, top-right, bottom-left, bottom-right.
    - w (int): Width of the output image.
    - h (int): Height of the output image.

    Returns:
    - np.ndarray: Warped image.
    """
    dst_points = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    return cv2.warpPerspective(image, matrix, (w, h))

@functions_framework.http
def main(request: flask.Request) -> flask.Response:
    """
    HTTP Cloud Function to warp an image given a URL and source points.

    Args:
    - request (flask.Request): The Flask request object.

    Returns:
    - flask.Response: The Flask response object.
    """
    request_json = request.get_json(silent=True)
    image_url = request_json.get("url")
    src_points = np.float32(request_json.get("src_points"))
    width = request_json.get("width")
    height = request_json.get("height")

    if not image_url:
        return "Image URL is required", 400

    try:
        image = read_image_from_url(image_url)
        warped = warp_image(image, src_points, width, height)
        is_ok, buffer = cv2.imencode(".jpg", warped)
        if not is_ok:
            return "Error converting image to JPEG format", 500
        byte_io = BytesIO(buffer)
        return send_file(byte_io, mimetype="image/jpeg")
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
