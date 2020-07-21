from PyQt5 import QtWidgets
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
from


# from .settings import TCP_PORT


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


class ChatWindow(QtWidgets.QMainWindow):
    protocol: ConnectorProtocol
    reactor = None
    ui:win.Window

    def __init__(self):
        super().__init__()
        self.ui = win.Window()
        self.ui.setupUi(self)

def main():
    app = QtWidgets.QApplication([])
    application = ChatWindow()
    application.show()
    app.exec()

if __name__ == '__main__':
    main()
