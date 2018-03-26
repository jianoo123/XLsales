import xadmin
from .models import Documents

class DocumentsAdmin(object):
    list_display = ['document_id','client', 'district', 'money', 'add_time']
    search_field = ['client', 'district', 'money']
    list_filter =  ['client', 'district', 'money']


xadmin.site.register(Documents,DocumentsAdmin)