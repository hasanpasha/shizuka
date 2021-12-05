


from functools import lru_cache
import pkgutil
import inspect
import importlib
import os
from operator import itemgetter
from enum import Enum, auto
from abc import ABC

__VERSION = "0.0.1"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'




class Status(Enum):
    """Status types"""
    ENABLED = auto()
    DISABLED = auto()


# The base class
class Server(ABC):
    id: str
    name: str

    headers = None
    session_expiration_cookies = []
    status: Status = Status.ENABLED  # ENABLED by default

    base_url = None

    __sessions = {}

    @property
    def session(self):
        return self.__sessions.get(self.id)

    @session.setter
    def session(self, session):
        print("Setting Session")
        self.__sessions[self.id] = session

    def session_get(self, *args, **kwargs):
        """ Get data method """
        try:
            resp = self.session.get(*args, **kwargs)
        except:
            raise

        return resp        

    
@lru_cache()
def get_servers_list(include_disabled=False, order_by=('name')):
    import api.servers

    def iter_namespace(ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + '.')

    servers = []
    for _finder, name, _ispkg in iter_namespace(api.servers):
        module = importlib.import_module(name)
        for _name, obj in dict(inspect.getmembers(module)).items():
            if not hasattr(obj, 'id') or not hasattr(obj, 'name'):
                continue
            if NotImplemented in (obj.id, obj.name):
                continue

            if not include_disabled and obj.status == Status.DISABLED:
                continue

            if inspect.isclass(obj) and obj.__module__.startswith('api.servers.'):
                # logo_path = os.path.join(os.path.dirname(os.path.abspath(
                #     module.__file__)), get_server_main_id_by_id(obj.id) + '.ico')

                servers.append(dict(
                    id=obj.id,
                    name=obj.name,
                    class_name=get_server_class_name_by_id(obj.id),
                    module=module,
                ))

    # print(servers)

    # return sorted(servers, key=itemgetter(*order_by))
    return servers


def get_server_class_name_by_id(id):
    return id.split(':')[0].capitalize()

def get_server_main_id_by_id(id) -> str:
    return id.split(':')[0].split('_')[0]
