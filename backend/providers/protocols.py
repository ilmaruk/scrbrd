import typing


class ConnectionsProvider(typing.Protocol):
    def put(self, connection):
        ...

    def delete(self, connection_id):
        ...
