import xadmin
from .models import Clients

class ClientsAdmin(object):
    list_display = ['name','district','add_time']
    search_field = ['name']
    list_filter = ['name']


xadmin.site.register(Clients,ClientsAdmin)