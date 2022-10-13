import decimal
import json
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, _context):
    print("EVENT", event)

    request_context = event.get("requestContext", {})
    connection_id = request_context.get("connectionId")

    board_id = json.loads(event.get("body", "{}")).get("boardId")

    board = {"a": board_id}  # TODO: get from DB

    api_gateway_management_api = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url="https://" + os.environ.get("APIG_ENDPOINT"))
    api_gateway_management_api.post_to_connection(
        Data=json.dumps(board, cls=DecimalEncoder), ConnectionId=connection_id)

    return {}


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
