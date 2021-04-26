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
from dict.models import ReportError
#--Edit your configuration here ------------------------------
username = urllib.parse.quote_plus('')
password = urllib.parse.quote_plus('')
auth_db = urllib.parse.quote_plus('')
server = urllib.parse.quote_plus('')
port = urllib.parse.quote_plus('27017')
#-------------------------------------------------------------
clickstream_client = MongoClient(f'mongodb://{username}:{password}@{server}:{port}/?authSource={auth_db}')
# clickstream_collection = clickstream_client['newsfeed2']

clickstream_client = MongoClient('docker.for.mac.host.internal',27017)
pantip_ingredients = clickstream_client['pantip_recipes']

@login_required()
def index(request):
    page="dict"

    ingredient_dict = pantip_ingredients["ingredient_dict"]
    for i in ingredient_dict.find().sort("$natural", -1).limit(1):
        ingredient_dict_data=i
        last_update=datetime.datetime.strptime(i["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")

        ingredient_dict_data.pop("_id")
        ingredient_dict_data.pop("timestamp")
    context={"page":page,"ingredient_dict_data":ingredient_dict_data,"last_update":last_update}
    return render(request,'dict.html',context)

@login_required()
def errorlist(request):
    page="error"
    report = ReportError()
    report.pantip_id="40429383"
    report.report_data="messagedata"
    report.save()
    print(report)
    user =[ ]
    # user = ReportError().objects
    print(ReportError())
    context={"page":page,"list_user":user}
    return render(request,'error_list.html',context)