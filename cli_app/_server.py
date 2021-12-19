
from . import ServerUtils
from . import prompt

def _choose_server(self):
    if self.server != None:
        return

    su = ServerUtils()
    servers = su.servers_list
    servers_ids = [dict(name=server['id']) for server in servers]

    answers = prompt([
        {
            'name': 'server_name',
            'type': 'list',
            'message': 'choose server: ',
            'choices': servers_ids,
            'when': lambda _: len(servers) > 1
        }
    ])

    try:
        cls = su.get_class_by_id(answers['server_name'])
    except KeyError:
        print(
            f"Selected {servers_ids[0]['name']}, 'cause there is only one server... ")
        cls = su.get_class_by_id(servers_ids[0]['name'])

    if cls == None:
        print("Error on getting a class... ")
        exit(1)

    self.server = cls
