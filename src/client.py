from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver

from .settings import TCP_PORT

class ConnectorProtocol(LineOnlyReceiver):
    factory: "Connector"

    def connectionMade(self):
        self.factory.window.protocol = self
        pass

    def lineReceived(self, line):
        message = line.decode(encoding='utf-8')
        pass


class Connector(ClientFactory):
    window: 'ChatWindow'
    protocol: ConnectorProtocol
    pass


class ChatWindow:
    protocol: ConnectorProtocol
    reactor = None
