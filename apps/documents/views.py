# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
import datetime
from django.db.models import Q

from .models import Documents
from clients.models import District,Clients
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