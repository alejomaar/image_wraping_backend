import base64
import cv2
import numpy as np
import functions_framework



def base64_to_img(base64_image: str):
    image_data = base64.b64decode(base64_image)

    # Convert bytes data to a numpy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Read image from numpy array
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

@functions_framework.http
def main(request: dict):
    """HTTP Cloud Function for POST requests.
    Args:
        request (flask.Request): The request object.
    """
    # Assume the event dictionary has the base64 string under a key 'image'
    
    
    if request.method != 'POST':
        return 'This function only accepts POST requests.', 405
    
    data = request.get_json()
    base64_image = data['image']

    image = base64_to_img(base64_image)

    # Process the image if necessary
    # (In this case, no processing is done)

    # Re-encode the image to base64
    _, buffer = cv2.imencode(".jpg", image)
    encoded_image = base64.b64encode(buffer).decode()

    return encoded_image
