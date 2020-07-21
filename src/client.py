from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver

from .server import TCP_PORT

class ConnectorProtocol(LineOnlyReceiver):
    factory: "Connector"
    pass

class Connector(ClientFactory):
    protocol:ConnectorProtocol
    pass