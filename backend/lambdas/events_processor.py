import json
import boto3
import os

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    """Process new events.
    """
    records = event.get("Records", [])
    if len(records) == 0:
        return {}

    event = records[0].get("dynamodb", {}).get("NewImage", {})
    print("Event to process", event)

    return {}
