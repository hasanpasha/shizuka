
from api import factory
from api.factory import Factory

FACTORY_INITIATED: bool = False

def get_class_by_id(id: str):

    # Get class info from list of servers
    def get_class_info(id: str):
        for server in get_list_of_servers():
            if server['id']:
                return server

    return factory.get_server_class(get_class_info(id))

def initiate_factory():
    global FACTORY_INITIATED
    if not FACTORY_INITIATED:
        global factory
        factory = Factory()
        FACTORY_INITIATED = True

def get_list_of_servers():
    initiate_factory()
    return factory.servers_list
    
def list_servers():
    servers_list = get_list_of_servers()

    for server in servers_list:
        print(server['id'])

def get_id_list():
    servers_list = get_list_of_servers()
    return [server['id'] for server in servers_list]