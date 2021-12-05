
from api.servers import Server
from api.servers import Status

class Vodu(Server):
    id = 'vodu'
    name = "Vodu"
    status = Status.DISABLED
