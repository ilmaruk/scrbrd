from .providers import ConnectionsProvider


class DynamoDBConnectionsProvider(ConnectionsProvider):
    def __init__(self, table):
        self._table = table

    def put(self, connection):
        return self._table.put_item(Item=connection)

    def delete(self, connection_id):
        return self._table.delete_item(Key={"connectionId": connection_id})
