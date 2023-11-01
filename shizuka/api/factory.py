
from shizuka.api import servers
from typing import List

class Factory:
    """This will handle the servers"""

    @property
    def servers_list(self) -> List:
        list_of_servers = servers.get_servers_list()
        if list_of_servers != None:
            return list_of_servers

    def get_server_class(self, server_info: dict):
        module = server_info['module']
        class_name = server_info['class_name']

        # get an instance of server class
        cls = getattr(module, class_name)()
        if cls != None:
            return cls
            
        
