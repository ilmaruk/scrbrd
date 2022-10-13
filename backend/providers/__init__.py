import os

import boto3

from .protocols import ConnectionsProvider
from .dynamodb import DynamoDBConnectionsProvider


def get_connections_provider(driver: str) -> ConnectionsProvider:
    if driver == "dynamodb":
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(os.environ.get("CONNECTIONS_TABLE"))
        return DynamoDBConnectionsProvider(table)
