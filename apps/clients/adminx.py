import xadmin
from .models import Clients

class ClientsAdmin(object):
    list_display = ['name','address','add_time']
    search_field = ['name','address']
    list_filter = ['name','address']


xadmin.site.register(Clients,ClientsAdmin)