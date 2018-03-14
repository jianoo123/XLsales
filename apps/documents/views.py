# _*_ encoding:utf-8 _*_
import datetime
import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from clients.models import District
from commodities.models import Factory, FactoryToCommodity, RelateCharge
from .models import Documents


# Create your views here.
class HomePageView(View):
    def get(self,request):
        check = request.GET.get('check','')
        client = request.GET.get('client', '显示全部')
        year = datetime.date.today().year
        month = datetime.date.today().month
        all_districts = District.objects.all()
        all_documents = Documents.objects.all()
        if check == '':
            if client == '显示全部':
                all_documents = all_documents.filter(add_time__year=year).order_by('-add_time')
            else:
                all_documents = Documents.objects.filter(Q(client__name=client) | Q(district__name=client))
                all_documents = all_documents.filter(add_time__year=year).order_by('-add_time')
        if check == '3':
            if client == '显示全部':
                all_documents = all_documents.filter(add_time__year=month).order_by('-add_time')
            else:
                all_documents = Documents.objects.filter(Q(client__name=client) | Q(district__name=client))
                all_documents = all_documents.filter(add_time__year=month).order_by('-add_time')
        return render(request,'index.html',{
            'all_districts':all_districts,
            'check_num':check,
            'all_documents':all_documents,

        })


class AddDocument(View):
    def get(self, request):
        factory_commodity = request.GET.get('commodities', '').split(' ',1)
        if len(factory_commodity)>1:
            commodity_request = factory_commodity[0]
            factory_request = factory_commodity[1]
            product = FactoryToCommodity.objects.filter(commodity__name=commodity_request,factory__name=factory_request)
            all_relate = RelateCharge.objects.filter(factory=product)
            charge = {}
            i = 0
            for relate in all_relate:
                charge['charge'+str(i)] = relate.charge.charge
                i += 1
            return HttpResponse(json.dumps(charge),content_type='application/json')
        else:
            factories = Factory.objects.all()
            return render(request, 'document.html', {
                'factories': factories,
            })

    def post(self,request):
        all_merchant = request.POST.getlist('merchant','')
        all_charge = request.POST.getlist('charge','0')
        all_sales_nums = request.POST.getlist('sale_nums','0')
        ownmoney = request.POST.get('ownmoney', 0)
        payback = request.POST.get('payback', 0)
        return HttpResponseRedirect(reverse('index') )