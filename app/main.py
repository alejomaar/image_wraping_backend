import base64
import cv2
import numpy as np

def main(event: dict):
    # Assume the event dictionary has the base64 string under a key 'image'
    base64_image = event['image']

    # Decode the base64 string to bytes
    image_data = base64.b64decode(base64_image)

    # Convert bytes data to a numpy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Read image from numpy array
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Process the image if necessary
    # (In this case, no processing is done)

    # Re-encode the image to base64
    _, buffer = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(buffer).decode()

    return encoded_image

