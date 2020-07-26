COUNT_MESSAGE_SEND_ON_LOGIN = 10
TCP_PORT = 7410
DEFAULT_CONNECT_TO = 'localhost'
FILE_SETTINGS = 'chat.ini'

init_states = {'count_messages_send_on_login': COUNT_MESSAGE_SEND_ON_LOGIN,
               'tcp_port': TCP_PORT,
               'connect_to': DEFAULT_CONNECT_TO,
               'client_window': [300,300,300,500]
               }


def parce_ini():
    global init_states
    with open(FILE_SETTINGS,'rt') as ini_file:
        for line in ini_file:
            line = line[:-1]
            key,value = line.split(':')
            if key == 'count_messages_send_on_login':
                value = int(value)
            elif key == 'tcp_port':
                value = int(value)
            elif key == 'client_window':
                value =[ int(x) for x in value.split(',')]
            init_states[key] = value


def get_init_states():
    global init_states
    try:
        parce_ini()
    except FileNotFoundError as exc:
        print(str(exc))
    return init_states


def save_init_states():
    with open(FILE_SETTINGS,'wt',encoding="utf-8") as ini_file:
        for key,value in init_states.items():
            if key=='client_window':
                print(f'{key}:{value[0]},{value[1]},{value[2]},{value[3]}',sep='',file=ini_file)
            else:
                print(f'{key}:{value}',file=ini_file,sep='')


if __name__ == '__main__':
    ret = get_init_states()
    print(ret)
    save_init_states()


