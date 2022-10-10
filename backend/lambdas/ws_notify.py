import json
import boto3
import os

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    print("EVENT", event)
    print("CONTEXT", context)

    request_context = event.get("requestContext", {})

    records = event.get("Records", [])
    print("RECORDS", records)
    if len(records) == 0:
        return {}

    board = records[0].get("dynamodb", {}).get("NewImage", {})
    board_id = board.get("boardId", {}).get("S")
    print("BOARD", board)
    print("BOARD_ID", board_id)

    paginator = dynamodb.get_paginator("scan")

    connections = []
    for page in paginator.paginate(
            TableName=os.environ.get("CONNECTIONS_TABLE")):
        connections.extend(page.get("Items", []))

    print("Connections",
          [c.get("connectionId", {}).get("S") for c in connections])

    # TODO: automatic endpoint or from env
    api_gateway_management_api = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url="https://hgbtog98rf.execute-api.eu-south-1.amazonaws.com/"
                     "dev")
    for connection in connections:
        print("CONNECTION", connection)
        # TODO: scan only matching documents
        connection_board_id = connection.get("boardId", {}).get("S")
        if connection_board_id != board_id:
            continue

        connection_id = connection.get("connectionId", {}).get("S")
        print(f"Sending message '{board}' to connection {connection_id} ...")
        api_gateway_management_api.post_to_connection(
            Data=json.dumps(board), ConnectionId=connection_id)
        print(f"Sent message '{board}' to connection {connection_id} ...")

    return {}
