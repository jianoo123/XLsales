import xadmin
from .models import Commodities

class CommoditiesAdmin(object):
    list_display = ['name', 'charge', 'factory', 'add_time']
    search_field = ['name', 'factory']
    list_filter = ['name', 'factory']


xadmin.site.register(Commodities,CommoditiesAdmin)