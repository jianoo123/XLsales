import xadmin
from .models import Documents

class DocumentsAdmin(object):
    list_display = ['client', 'commodities', 'document_id', 'add_time']
    search_field = ['client', 'commodities']
    list_filter = ['client', 'commodities']


xadmin.site.register(Documents,DocumentsAdmin)