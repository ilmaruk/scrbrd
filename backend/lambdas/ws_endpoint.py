import boto3
import os

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    print("EVENT", event)
    print("CONTEXT", context)

    request_context = event.get("requestContext", {})
    route_key = request_context.get("routeKey")
    connection_id = request_context.get("connectionId")

    query_string_parameters = event.get("queryStringParameters", {})
    board_id = query_string_parameters.get("boardId")
    print("BOARD_ID", board_id)

    connections_table = dynamodb.Table(os.environ.get("CONNECTIONS_TABLE"))

    if route_key == "$connect":
        connections_table.put_item(
            Item={"connectionId": connection_id, "boardId": board_id})
    elif route_key == "$disconnect":
        connections_table.delete_item(
            Key={"connectionId": connection_id})
    else:
        # TODO: return an error
        pass

    return {}
