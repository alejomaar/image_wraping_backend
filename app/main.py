import base64
import json


def decode_pubsub_message(event: dict):
    try:
        if "data" not in event:
            raise ValueError("No 'data' key in the event")

        pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        data = json.loads(pubsub_message)
        return data

    except ValueError as ve:
        print("ValueError: {}".format(str(ve)))
    except json.JSONDecodeError as je:
        print("JSONDecodeError: {}".format(str(je)))
    except Exception as e:
        print("Unexpected Error: {}".format(str(e)))


def main(event: dict, context):
    print(
        "BEGIN messageId {} published at {}".format(context.event_id, context.timestamp)
    )

    pub_sub_message = decode_pubsub_message(event)
    print(pub_sub_message)
    return pub_sub_message
