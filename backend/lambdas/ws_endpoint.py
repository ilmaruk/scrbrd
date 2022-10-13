import boto3

from ..providers import get_connections_provider

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    request_context = event.get("requestContext", {})
    route_key = request_context.get("routeKey")
    connection_id = request_context.get("connectionId")

    query_string_parameters = event.get("queryStringParameters", {})
    board_id = query_string_parameters.get("boardId")

    provider = get_connections_provider("dynamodb")

    if route_key == "$connect":
        provider.put({"connectionId": connection_id, "boardId": board_id})
    elif route_key == "$disconnect":
        provider.delete(connection_id)
    else:
        # TODO: return an error
        pass

    return {}
