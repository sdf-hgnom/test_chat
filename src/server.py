from collections import deque

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver

from src.settings import get_init_states

COUNT_MESSAGE_SEND_ON_LOGIN = 10


class Handler(LineOnlyReceiver):
    factory: 'Server'
    login: str
    init_states :dict = get_init_states()

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)
        print('Connect Lost')

    def connectionMade(self):
        self.login = None
        self.factory.clients.append(self)
        print(f'Connect Made from {self.transport.client[0]} ')

    def send_history(self, num_of_messages):
        if len(self.factory.get_logins()) > 1:
            current_mess = deque(self.factory.history.copy(), maxlen=num_of_messages)
            for message in current_mess:
                self.sendLine(message.encode(encoding='utf-8'))

    def is_free_login(self, login):
        return login not in self.factory.get_logins()

    def lineReceived(self, line):
        print(f'Get message :{line}')
        if line and line[0] != 0xff:
            message = line.decode(encoding='utf-8')
        else:
            return
        if self.login is not None:
            message = f'<{self.login}> : {message}'
            self.factory.history.append(message)
            for user in self.factory.clients:
                if user is not self:
                    user.sendLine(message.encode(encoding='utf-8'))
        else:

            if message.startswith('login:'):
                user_name = message.replace('login:', '')
                if self.is_free_login(login=user_name):
                    self.login = user_name
                    print(f'New user {self.login}')
                    return_message = f'Привет {self.login} Сейчас всего {len(self.factory.clients)} пользователнй здесь'
                    self.sendLine(return_message.encode(encoding='utf-8'))
                    self.send_history(COUNT_MESSAGE_SEND_ON_LOGIN)
                else:
                    self.sendLine(f'логин {user_name} занят - попробуйте другой'.encode(encoding='utf-8'))
            else:
                self.sendLine('Неверный логин'.encode(encoding='utf-8'))


class Server(ServerFactory):
    protocol = Handler
    clients: list
    history: deque

    def get_logins(self) -> list:
        current_users = []
        for user in self.clients:
            current_users.append(user.login)
        return current_users

    def startFactory(self) -> None:
        print('Start Server ......')

    def __init__(self) -> None:
        self.clients = []
        self.history = deque(maxlen=100)


def run_server(what_port: int) -> None:
    server: Server = Server()
    reactor.listenTCP(what_port, server)
    reactor.run()


if __name__ == '__main__':
    init_states: dict = get_init_states()
    run_server(what_port=init_states['tcp_port'])
