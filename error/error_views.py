# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
import os
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.urls import reverse
import pytz
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient
import urllib
from error.models import Report
from django.contrib import messages
import requests
#--Edit your configuration here ------------------------------
username = urllib.parse.quote_plus('')
password = urllib.parse.quote_plus('')
auth_db = urllib.parse.quote_plus('')
server = urllib.parse.quote_plus('')
port = urllib.parse.quote_plus('27017')
#-------------------------------------------------------------
# clickstream_client = MongoClient(f'mongodb://{username}:{password}@{server}:{port}/?authSource={auth_db}')
# clickstream_collection = clickstream_client['newsfeed2']
clickstream_client = MongoClient('docker.for.mac.host.internal',27017)
pantip_ingredients = clickstream_client['pantip_recipes']

@login_required()
def index(request):
    page="error"
    # report = Report()
    # report.pantip_id="40429383"
    # report.report_data="messagedata"
    # report.save()
    user =[ ]
    user = Report().__class__.objects.all()
    # user = Report().__class__.objects.filter(status="wait")
    # print(user)
    context={"page":page,"list_user":user}
    return render(request,'error_list.html',context)

@login_required()
def delete_report(request, id):
    report = Report().__class__.objects.filter(id=id).first()
    if report is None:
        messages.add_message(request, messages.ERROR, 'Error Delete Report' )
        return HttpResponseRedirect(reverse('error:index'))
    report.delete()
    messages.add_message(request, messages.INFO, 'Delete Report Successful')
    return HttpResponseRedirect(reverse('error:index'))

@login_required()
def DataList(request):
    page="datalist"
    
    testdata=[]
    recipe_data = pantip_ingredients["recipe_data"]
    for i in recipe_data.find():
        testdata.append(i) 
    # report = Report().__class__.objects.filter(id=id).first()
    # if report is None:
    #     messages.add_message(request, messages.ERROR, 'Error Delete Report' )
    #     return HttpResponseRedirect(reverse('error:index'))
    # report.delete()
    # messages.add_message(request, messages.INFO, 'Delete Report Successful')
    context={"page":page,"list_data":testdata}
    return render(request,'data_list.html',context)

@login_required()
def editDataList(request,id):
    page="datalist"
    
    recipe_data = pantip_ingredients["recipe_data"]
    for i in recipe_data.find({"id":id}).limit(1):
        testdata=i
    # report = Report().__class__.objects.filter(id=id).first()
    # if report is None:
    #     messages.add_message(request, messages.ERROR, 'Error Delete Report' )
    #     return HttpResponseRedirect(reverse('error:index'))
    # report.delete()
    # messages.add_message(request, messages.INFO, 'Delete Report Successful')
    context={"page":page,"list_data":testdata}
    return render(request,'data_edit.html',context)

@login_required()
def update_data(request,id):
    try:
        recipe_data = pantip_ingredients["recipe_data"]

        title=request.GET.get('title')
        imagelink=request.GET.get('imagelink')
        ingredients=request.GET.get('ingredients')
        # print(title,imagelink,ingredients)
        ingredients=ingredients.split(",")
        # point=request.GET.get('point')
        # desc=request.GET.get('desc')

        # content_json = json.loads(url.text)
        # desc = content_json["_source"]["desc_full"]
        # point = content_json["_source"]["point"]

        newvalues = { "$set": { "title": title,"imagelink":imagelink,"ingredients":ingredients} }
        recipe_data.update_one({"id":id}, newvalues)
        messages.add_message(request, messages.INFO, 'Update Data Successful')
        # return HttpResponseRedirect(reverse('error:editDataList',kwargs={'id':id}))
        return HttpResponseRedirect(reverse('error:DataList'))
    except:
        messages.add_message(request, messages.ERROR, 'Error Update Data' )

        return HttpResponseRedirect(reverse('error:editDataList',kwargs={'id':id}))

@login_required()
def editReport(request,reportid,id):
    page="error"
    
    recipe_data = pantip_ingredients["recipe_data"]
    # print(reportid,id)
    testdata=[]
    for i in recipe_data.find({ "id": id }).limit(1):
        testdata=i
    # report = Report().__class__.objects.filter(id=id).first()
    # if report is None:
    #     messages.add_message(request, messages.ERROR, 'Error Delete Report' )
    #     return HttpResponseRedirect(reverse('error:index'))
    # report.delete()
    # messages.add_message(request, messages.INFO, 'Delete Report Successful')
    
        
        # messages.add_message(request, messages.ERROR, 'Not Found This tid' )
        
        # return HttpResponseRedirect(reverse('error:index'))
    # print(testdata)
    if testdata!=[]:
        context={"page":page,"list_data":testdata,"reportid":reportid}
        return render(request,'data_edit.html',context)
    else:
        report = Report().__class__.objects.filter(id=reportid).first()
        if report is None:
            messages.add_message(request, messages.ERROR, 'Not Found This tid And Error Delete Report' )
            return HttpResponseRedirect(reverse('error:index'))
        # report.delete()
        messages.add_message(request, messages.INFO, 'Not Found This tid And Delete Report Successful')
        return HttpResponseRedirect(reverse('error:index'))





    context={"page":page,"list_data":testdata}
    return render(request,'data_edit.html',context)

@login_required()
def update_report(request,reportid,id):
    try:
        recipe_data = pantip_ingredients["recipe_data"]

        title=request.GET.get('title')
        imagelink=request.GET.get('imagelink')
        ingredients=request.GET.get('ingredients')

        # point=request.GET.get('point')
        # desc=request.GET.get('desc')
        # content_json = json.loads(url.text)
        # desc = content_json["_source"]["desc_full"]
        # point = content_json["_source"]["point"]

        ingredients=ingredients.split(",")
        newvalues = { "$set": { "title": title,"imagelink":imagelink,"ingredients":ingredients} }

        recipe_data.update_one({"id":id}, newvalues)
        report = Report().__class__.objects.filter(id=reportid).first()
        if report is None:
            messages.add_message(request, messages.ERROR, 'Error Update Data' )
            return HttpResponseRedirect(reverse('error:index'))
        # report.delete()
        report.status="updated"
        report.edit_user="nichakarn.ra@ku.th"
        report.save()
        messages.add_message(request, messages.INFO, 'Update Data Successful')
        return HttpResponseRedirect(reverse('error:index'))
    except:
        messages.add_message(request, messages.ERROR, 'Error Update Data' )
        return HttpResponseRedirect(reverse('error:index'))
    

@login_required()
def delete_data(request, id):
    try:
        recipe_data = pantip_ingredients["recipe_data"]
        recipe_data.delete_one({"id":id})
        messages.add_message(request, messages.INFO, 'Delete Report Successful')
    except:
        messages.add_message(request, messages.ERROR, 'Error Delete Report' )
        return HttpResponseRedirect(reverse('error:DataList'))

    return HttpResponseRedirect(reverse('error:DataList'))
