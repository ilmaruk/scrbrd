import boto3
import os

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    print("EVENT", event)
    print("CONTEXT", context)

    request_context = event.get("requestContext", {})

    route_key = request_context.get("routeKey")
    connection_id = request_context.get("connectionId")

    if route_key == "$connect":
        dynamodb.put_item(
            TableName=os.environ.get("CONNECTIONS_TABLE"),
            Item={"connectionId": {"S": connection_id}}
        )
    elif route_key == "$disconnect":
        dynamodb.delete_item(
            TableName=os.environ.get("CONNECTIONS_TABLE"),
            Key={"connectionId": {"S": connection_id}}
        )

    return {}
