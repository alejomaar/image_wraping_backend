from io import BytesIO

import cv2
import flask
import functions_framework
import numpy as np
import requests
from flask import make_response, send_file
from pydantic import BaseModel, Field, HttpUrl, ValidationError


class Body(BaseModel):
    src_points: list[list[float]]
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    url: HttpUrl


def read_image_from_url(url: str) -> np.ndarray:
    """
    Reads an image from a given URL.

    Args:
    - url (str): URL of the image to be downloaded.

    Returns:
    - np.ndarray: The image as a NumPy array.
    """
    response = requests.get(url, timeout=20)
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
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }
    try:
        if request.method == "OPTIONS":
            # Allows GET requests from any origin with the Content-Type
            # header and caches preflight response for an 3600s
            print("Enter headers ")
            return ("", 204, headers)

        request_json = request.get_json(silent=True)
        body = Body(**request_json)

        image = read_image_from_url(body.url)
        h,w, _ = image.shape
        src_points = np.float32(body.src_points)
        src_points[:, 0] *= w
        src_points[:, 1] *= h
        warped = warp_image(image, src_points, body.width, body.height)
        is_ok, buffer = cv2.imencode(".jpg", warped)
        if not is_ok:
            return "Error converting image to JPEG format", 500
        byte_io = BytesIO(buffer)
        response = make_response(send_file(byte_io, mimetype="image/jpeg"))
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except ValidationError as e:
        return f"Body format is incorrect: {e.errors()}", 400

    except Exception as e:
        return f"An error occurred: {str(e)}", 500
