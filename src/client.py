from PyQt5 import QtWidgets
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
from src.gui.window import Window


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
    ui: Window

    def __init__(self):
        super().__init__()
        self.ui = Window()
        self.ui.setupUi(self)
        self.setup_events()

    def button_click(self):
        message = self.ui.lineEdit.text()
        self.ui.lineEdit.clear()
        self.ui.plainTextEdit.appendPlainText(message)

    def exit_button_click(self):
        self.close()

    def setup_events(self):
        self.ui.pushButton.clicked.connect(self.button_click)


def main():
    app = QtWidgets.QApplication([])
    application = ChatWindow()
    application.show()
    app.exec()


if __name__ == '__main__':
    main()
