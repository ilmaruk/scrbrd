import json
import os
import uuid

import boto3

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    """Store a new event on the event table
    """
    event = json.loads(event.get("body", "{}"))
    # TODO: validate event

    event["eventId"] = str(uuid.uuid4())

    events_table = dynamodb.Table(os.environ.get("EVENTS_TABLE"))
    events_table.put_item(Item=event)

    return {
        "statusCode": 201
    }
