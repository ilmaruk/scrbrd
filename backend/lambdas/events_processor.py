import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    """Process new events.
    """
    records = event.get("Records", [])
    if len(records) == 0:
        return {}

    boards_table = dynamodb.Table(os.environ.get("BOARDS_TABLE"))

    for record in records:
        update_item(record, boards_table)

    return {}


def update_item(record, table) -> None:
    raw = record.get("dynamodb", {}).get("NewImage", {})
    td = TypeDeserializer()
    event = {k: td.deserialize(v) for k, v in raw.items()}

    if event["eventType"] == "SCORE":
        board_id = event["boardId"]
        contender = event["contender"]
        value = event["value"]
        table.update_item(
            Key={"boardId": board_id},
            UpdateExpression=f"SET scores[{contender}] = "
                             f"scores[{contender}] + :val",
            ExpressionAttributeValues={":val": value}
        )
