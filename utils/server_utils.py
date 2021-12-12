
from api.factory import Factory
from typing import List


class ServerUtils:

    def __init__(self) -> None:
        self.factory = Factory()

    def get_class_by_id(self, id: str):

        # Get class info from list of servers
        def get_class_info(id: str):
            for server in self.servers_list:
                if server['id']:
                    return server

        return self.factory.get_server_class(get_class_info(id))

    @property
    def servers_list(self):
        return self.factory.servers_list
        
    def list_servers(self):
        for server in self.servers_list:
            print(server['id'])

    @property
    def get_id_list(self) -> List:
        return [server['id'] for server in self.servers_list]
