import xadmin
from .models import Commodities

class CommoditiesAdmin(object):
    list_display = ['name', 'charge', 'add_time']
    search_field = ['name']
    list_filter = ['name']


xadmin.site.register(Commodities,CommoditiesAdmin)