# _*_ encoding:utf-8 _*_
import datetime
import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from clients.models import District,Clients
from commodities.models import Factory, FactoryToCommodity, RelateCharge,Charge,Commodities
from .models import Documents,Documents_tr
from extra_apps.get_id import GetId


# Create your views here.
class HomePageView(View):
    def get(self,request):
        check = request.GET.get('check','')
        client = request.GET.get('client', '显示全部')
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
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
                all_documents = all_documents.filter(add_time__month=month).order_by('-add_time')
            else:
                all_documents = Documents.objects.filter(Q(client__name=client) | Q(district__name=client))
                all_documents = all_documents.filter(add_time__month=month).order_by('-add_time')
        return render(request,'index.html',{
            'all_districts':all_districts,
            'check_num':check,
            'all_documents':all_documents,

        })


class AddDocument(View):
    def get(self, request):
        factory_commodity = request.GET.get('commodities', '').split(' ',1)
        district = request.GET.get('district','')
        clients = Clients.objects.filter(district__name=district)
        districts = District.objects.all()
        if len(district)>0:
            client_name = {}
            j = 0
            for client in clients:
                client_name[j] = client.name
                j += 1
            return HttpResponse(json.dumps(client_name), content_type='application/json')
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
                'districts':districts,
                'clients':clients,
            })

    def post(self,request):
        district = request.POST.get('district','')#乡镇
        client = request.POST.get('client', '')#客户
        all_merchant = request.POST.getlist('merchant','')#商品名称列表
        all_charge = request.POST.getlist('charge','0')#价格列表
        all_sale_nums = request.POST.getlist('sale_nums','0')#销售数量列表
        all_merchant_sums = request.POST.getlist('merchant_sums', '')#商品总价列表
        salessums = request.POST.get('salessums', '')#销售总价
        all_returnmerchant_sums = request.POST.getlist('returnmerchant_sums', '')#退货商品总价列表
        return_sums = request.POST.get('return_sums', '')#退货总价
        ownmoney = request.POST.get('ownmoney', 0)#欠款
        payback = request.POST.get('payback', 0)#还款
        money = request.POST.get('money', 0)#总金额
        remark = request.POST.get('remark', 0)  # 总金额
        document = Documents()
        id = GetId().getid(district,client)
        document.document_id = id
        document.district = District.objects.get(name=district)
        document.client = Clients.objects.get(name=client)
        document.money = money
        document.ownmoney = ownmoney
        document.payback = payback
        document.remark = remark
        document.save()
        if len(all_merchant) == len(all_merchant_sums)+len(all_returnmerchant_sums):
            for i in range(0,len(all_merchant)):
                ################
                #销售部分
                ################
                if i < len(all_merchant_sums):
                    document_sale = Documents_tr()
                    document_sale.document_id = id
                    document_sale.classify = 'sale'
                    if len(all_merchant[i]) > 1:
                        merchant_name = all_merchant[i].split(' ',1)
                        #获取商品，如果数据库中没有则添加
                        try:
                            merchant = FactoryToCommodity.objects.get(factory__name=merchant_name[1],
                                                                     commodity__name=merchant_name[0])
                        except:
                            commodities_new = Commodities()
                            commodities_new.name = merchant_name[0]
                            commodities_new.save()
                            factory_new = Factory()
                            factory_new.name = merchant_name[1]
                            factory_new.save()
                            merchant = FactoryToCommodity()
                            merchant.factory = factory_new
                            merchant.commodity = commodities_new
                            merchant.save()
                        merchant_id = merchant.get_id()
                        # 商品价格，输入价格是新价格，则添加
                        if RelateCharge.objects.filter(factory=merchant, charge__charge=all_charge[i]):
                            document_sale.charge = all_charge[i]
                        else:
                            relatecharge = RelateCharge()
                            relatecharge.factory = merchant
                            if Charge.objects.filter(charge=all_charge[i]):
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            else:
                                charge = Charge()
                                charge.charge = all_charge[i]
                                charge.save()
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            relatecharge.save()
                            document_sale.charge = all_charge[i]
                    else:
                        merchant_name = ['','']
                        merchant_id = ''
                    document_sale.merchant_id = merchant_id #商品名称
                    document_sale.sale_nums = all_sale_nums[i] #商品数量
                    try:
                        document_sale.salessums = str(int(document_return.sale_nums) * int(document_return.charge))
                    except:
                        document_sale.salessums = 0
                    document_sale.save()
                ################
                #退货部分
                ################
                else:
                    document_return = Documents_tr()
                    document_return.document_id = id
                    document_return.classify = 'return'
                    if len(all_merchant[i]) > 1:
                        merchant_name = all_merchant[i].split(' ',1)
                        merchant = FactoryToCommodity.objects.filter(factory__name=merchant_name[1],
                                                                     commodity__name=merchant_name[0])[0]
                        merchant_id = merchant.get_id()
                        # 商品价格，输入价格是新价格，则添加
                        if RelateCharge.objects.filter(factory=merchant, charge__charge=all_charge[i]):
                            document_return.charge = all_charge[i]
                        else:
                            relatecharge = RelateCharge()
                            relatecharge.factory = merchant
                            if Charge.objects.filter(charge=all_charge[i]):
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            else:
                                charge = Charge()
                                charge.charge = all_charge[i]
                                charge.save()
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            relatecharge.save()
                            document_return.charge = all_charge[i]
                    else:
                        merchant_name = ['','']
                        merchant_id = ''
                    document_return.merchant_id = merchant_id #商品名称
                    document_return.sale_nums = all_sale_nums[i] #商品数量
                    try:
                        document_return.salessums = str(int(document_return.sale_nums) * int(document_return.charge))
                    except:
                        document_return.salessums = 0
                    document_return.save()
        return HttpResponseRedirect(reverse('index') )


class ChangeDocumentView(View):
    def get(self,request,document_id):
        factory_commodity = request.GET.get('commodities', '').split(' ',1)
        district = request.GET.get('district','')
        document = Documents.objects.get(document_id=document_id)
        districts = District.objects.all()
        clients = Clients.objects.filter(district=document.district)
        documentsale_trs = Documents_tr.objects.filter(document_id=document_id,classify='sale')
        documentreturn_trs = Documents_tr.objects.filter(document_id=document_id,classify='return')
        if len(district)>0:
            client_name = {}
            j = 0
            for client in clients:
                client_name[j] = client.name
                j += 1
            return HttpResponse(json.dumps(client_name), content_type='application/json')
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
        return render(request,'changedocument.html',{
            'factories': factories,
            'districts': districts,
            'clients': clients,
            'document':document,
            'documentsale_trs':documentsale_trs,
            "documentreturn_trs":documentreturn_trs,

        })

    def post(self,request,document_id):
        district = request.POST.get('district', '')  # 乡镇
        client = request.POST.get('client', '')  # 客户
        all_merchant = request.POST.getlist('merchant', '')  # 商品名称列表
        all_charge = request.POST.getlist('charge', '0')  # 价格列表
        all_sale_nums = request.POST.getlist('sale_nums', '0')  # 销售数量列表
        all_merchant_sums = request.POST.getlist('merchant_sums', '')  # 商品总价列表
        salessums = request.POST.get('salessums', '')  # 销售总价
        all_returnmerchant_sums = request.POST.getlist('returnmerchant_sums', '')  # 退货商品总价列表
        return_sums = request.POST.get('return_sums', '')  # 退货总价
        ownmoney = request.POST.get('ownmoney', 0)  # 欠款
        payback = request.POST.get('payback', 0)  # 还款
        money = request.POST.get('money', 0)  # 总金额
        remark = request.POST.get('remark', 0)  # 总金额
        document = Documents.objects.get(document_id=document_id)
        try:
            get_district = District.objects.get(name=district)
        except:
            get_district = District()
            get_district.name = district
            get_district.save()
        document.district = get_district
        try:
            get_client = Clients.objects.get(name=client)
        except:
            get_client = Clients()
            get_client.name = client
            get_client.district = get_district
            get_client.save()
        document.client = Clients.objects.get(name=client)
        document.money = money
        document.ownmoney = ownmoney
        document.payback = payback
        document.remark = remark
        document.add_time = datetime.datetime.today()
        document.save()
        if len(all_merchant) == len(all_merchant_sums) + len(all_returnmerchant_sums):
            for i in range(0, len(all_merchant)):
                ################
                # 销售部分
                ################
                if i < len(all_merchant_sums):
                    document_sale = Documents_tr()
                    document_sale.document_id = id
                    document_sale.classify = 'sale'
                    if len(all_merchant[i]) > 1:
                        merchant_name = all_merchant[i].split(' ', 1)
                        merchant = FactoryToCommodity.objects.filter(factory__name=merchant_name[1],
                                                                     commodity__name=merchant_name[0])[0]
                        merchant_id = merchant.get_id()
                        # 商品价格，输入价格是新价格，则添加
                        if RelateCharge.objects.filter(factory=merchant, charge__charge=all_charge[i]):
                            document_sale.charge = all_charge[i]
                        else:
                            relatecharge = RelateCharge()
                            relatecharge.factory = merchant
                            if Charge.objects.filter(charge=all_charge[i]):
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            else:
                                charge = Charge()
                                charge.charge = all_charge[i]
                                charge.save()
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            relatecharge.save()
                            document_sale.charge = all_charge[i]
                    else:
                        merchant_name = ['', '']
                        merchant_id = ''
                    document_sale.merchant_id = merchant_id  # 商品名称
                    document_sale.sale_nums = all_sale_nums[i]  # 商品数量
                    try:
                        document_sale.salessums = str(int(document_return.sale_nums) * int(document_return.charge))
                    except:
                        document_sale.salessums = 0
                    document_sale.save()
                ################
                # 退货部分
                ################
                else:
                    document_return = Documents_tr()
                    document_return.document_id = id
                    document_return.classify = 'return'
                    if len(all_merchant[i]) > 1:
                        merchant_name = all_merchant[i].split(' ', 1)
                        merchant = FactoryToCommodity.objects.filter(factory__name=merchant_name[1],
                                                                     commodity__name=merchant_name[0])[0]
                        merchant_id = merchant.get_id()
                        # 商品价格，输入价格是新价格，则添加
                        if RelateCharge.objects.filter(factory=merchant, charge__charge=all_charge[i]):
                            document_return.charge = all_charge[i]
                        else:
                            relatecharge = RelateCharge()
                            relatecharge.factory = merchant
                            if Charge.objects.filter(charge=all_charge[i]):
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            else:
                                charge = Charge()
                                charge.charge = all_charge[i]
                                charge.save()
                                relatecharge.charge = Charge.objects.filter(charge=all_charge[i])[0]
                            relatecharge.save()
                            document_return.charge = all_charge[i]
                    else:
                        merchant_name = ['', '']
                        merchant_id = ''
                    document_return.merchant_id = merchant_id  # 商品名称
                    document_return.sale_nums = all_sale_nums[i]  # 商品数量
                    try:
                        document_return.salessums = str(int(document_return.sale_nums) * int(document_return.charge))
                    except:
                        document_return.salessums = 0
                    document_return.save()
        return HttpResponseRedirect(reverse('index'))