import os

import boto3

from .ddb_connections_provider import DynamoDBConnectionsProvider

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    request_context = event.get("requestContext", {})
    route_key = request_context.get("routeKey")
    connection_id = request_context.get("connectionId")

    query_string_parameters = event.get("queryStringParameters", {})
    board_id = query_string_parameters.get("boardId")

    connections_table = dynamodb.Table(os.environ.get("CONNECTIONS_TABLE"))
    provider = DynamoDBConnectionsProvider(connections_table)

    if route_key == "$connect":
        provider.put({"connectionId": connection_id, "boardId": board_id})
    elif route_key == "$disconnect":
        provider.delete(connection_id)
    else:
        # TODO: return an error
        pass

    return {}
