from .protocols import ConnectionsProvider
from .dynamodb import DynamoDBConnectionsProvider


def get_connections_provider(driver: str, **kwargs) -> ConnectionsProvider:
    if driver == "dynamodb":
        return DynamoDBConnectionsProvider(kwargs["table"])
