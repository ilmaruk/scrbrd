import decimal
import json
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    records = event.get("Records", [])
    if len(records) == 0:
        return {}

    board = records[0].get("dynamodb", {}).get("NewImage", {})
    board_id = board.get("boardId", {}).get("S")

    paginator = dynamodb.get_paginator("scan")

    connections = []
    for page in paginator.paginate(
        TableName=os.environ.get("CONNECTIONS_TABLE"),
        IndexName="boardId",
        FilterExpression="#bid = :bid",
        ExpressionAttributeNames={"#bid": "boardId"},
        ExpressionAttributeValues={":bid": {"S": board_id}}
    ):
        connections.extend(page.get("Items", []))

    api_gateway_management_api = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url="https://" + os.environ.get("APIG_ENDPOINT"))
    for connection in connections:
        connection_board_id = connection.get("boardId", {}).get("S")
        if connection_board_id != board_id:
            continue

        connection_id = connection.get("connectionId", {}).get("S")
        api_gateway_management_api.post_to_connection(
            Data=serialise_board(board), ConnectionId=connection_id)

    return {}


def serialise_board(board) -> str:
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return str(o)
            return super(DecimalEncoder, self).default(o)

    td = TypeDeserializer()
    return json.dumps(
        {k: td.deserialize(v) for k, v in board.items()}, cls=DecimalEncoder)
