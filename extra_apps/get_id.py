from clients.models import District,Clients
from commodities.models import Factory, FactoryToCommodity, RelateCharge,Charge
from documents.models import Documents,Documents_tr
from datetime import datetime
class GetId():
    def getid(self,district,client):
        year = datetime.today().year
        month = datetime.today().month
        day = datetime.today().day
        today = str(year)+str(month)+str(day)
        district_id = District.objects.filter(name=district)[0].id
        client_id = Clients.objects.filter(name=client)[0].id
        count = Documents.objects.filter(district__name=district,client__name=client,add_time__year=year,add_time__month=month,add_time__day=day).count()
        id = today + str(district_id) + str(client_id) +str(count)
        return id