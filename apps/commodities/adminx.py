import xadmin
from .models import Commodities,FactoryToCommodity,Factory

class FactoryToCommodityAdmin(object):
    list_display = ['factory','commodity']
    search_field = ['factory','commodity']
    list_filter = ['factory','commodity']


class CommoditiesAdmin(object):
    list_display = ['name','add_time']
    search_field = ['name']
    list_filter = ['name']

class FactoryAdmin(object):
    list_display = ['name', 'add_time']
    search_field = ['name']
    list_filter = ['name']


xadmin.site.register(FactoryToCommodity,FactoryToCommodityAdmin)
xadmin.site.register(Commodities,CommoditiesAdmin)
xadmin.site.register(Factory,FactoryAdmin)