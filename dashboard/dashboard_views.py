# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
import os
from django.http import HttpResponse, HttpResponseRedirect
import datetime as dt
from django.urls import reverse
import pytz
from django.contrib.auth.decorators import login_required
from error.models import Report
from django.contrib import messages

from pymongo import MongoClient
import json
import urllib
import requests
import sys
from numpy import dot,isnan
from numpy.linalg import norm
from datetime import datetime
from django.views.static import serve
# from sklearn.metrics.pairwise import cosine_similarity

#--Edit your configuration here ------------------------------
username = urllib.parse.quote_plus('yok')
password = urllib.parse.quote_plus('yok100142')
auth_db = urllib.parse.quote_plus('admin')
server = urllib.parse.quote_plus('mars.mikelab.net')
port = urllib.parse.quote_plus('27017')
#-------------------------------------------------------------
clickstream_client = MongoClient(f'mongodb://{username}:{password}@{server}:{port}/?authSource={auth_db}')

clickstream_client = MongoClient('docker.for.mac.host.internal',27017)
# clickstream_collection = clickstream_client['newsfeed2']
pantip_ingredients = clickstream_client['pantip_recipes']


def index(request):
    page="dashboard"
    context={"page":page,}
    
    return render(request,'index.html',context) 


def pagedata(request,id):
    import timeit
    start = timeit.default_timer()
    page="pagedata"    
    url = requests.get("https://ptdev03.mikelab.net/kratooc/"+str(id))
    content_json = json.loads(url.text)
    desc_full = content_json["_source"]["desc_full"]

    import re
    reimage=re.compile('data-image="img:([0-9])*x([0-9])*"(\s*)')
    desc_full=reimage.sub('', desc_full)

    reimage=re.compile('width="([0-9])*"')
    desc_full=reimage.sub('width="100%"', desc_full)
    reimage=re.compile('height="([0-9])*"')
    desc_full=reimage.sub('height="100%"', desc_full)

    reimage=re.compile('class="img-in-post" ')
    desc_full=reimage.sub('height="100%" width="100%"', desc_full)
    ingredient_data=[]
    recipe_data = pantip_ingredients["recipe_data"]
    for i in recipe_data.find({ "id": id }):
        ingredient_data=(i["ingredients"])

    # full_ingredient_data=[]
    # for i in ingredient_data:
    #     try:
    #         full_ingredient_data.append(re.findall(i+'[ ก-๏]{0,9}[ ]*[½↉⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅐⅛⅜⅝⅞⅑⅒⅟0-9๐-๙]+[½↉⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅐⅛⅜⅝⅞⅑⅒⅟๐-๙0-9-+ /]*[ก-๏a-zA-Z]+', desc_full)[0])
            
    #     except :
    #         full_ingredient_data.append(i)
    testdata=[]
    # recipe_data = pantip_ingredients["recipe_data"]
    for i in recipe_data.find().sort("point",-1):
        testdata.append(i) 
############################  

    ingredient_dict = pantip_ingredients["ingredient_dict"]
    for i in ingredient_dict.find().sort("$natural", -1).limit(1):
        ingredient_dict_data=i

        ingredient_dict_data.pop("_id")
        ingredient_dict_data.pop("timestamp")
          
    fullwant=[]
    for i in ingredient_data:
        # b=0
        for j in  ingredient_dict_data:
            # if b == 1:
            #     break
            for k in ingredient_dict_data[j]:
                if i in ingredient_dict_data[j][k]:
                    fullwant+=ingredient_dict_data[j][k]
                    # b=1
                    # break
    # notwant=fullnotwant
    temp_data=[]
    for i in testdata:
        a=[1] * len(i["ingredients"])
        b=[]
        for j in i["ingredients"]:
            # print(j)
            if j in fullwant:
                b.append(1)
            else:
                b.append(0)
        cos_sim = dot(a, b)/(norm(a)*norm(b))
        if not isnan(cos_sim) and i['id']!=id:
            # print(cos_sim)
            temp_data.append({"cos_sim":cos_sim,"data":i})
    temp_data=sorted(temp_data, key = lambda i: i['cos_sim'],reverse=True)
    
    temp_data=[x["data"] for x in temp_data[:11]] 
    # print(temp_data)
    testdata=temp_data


    # context={"page":page,"id":id,"desc_full":desc_full,"title":content_json["_source"]["title"],"ingredient_data":ingredient_data,"simiarlity_kratoo":testdata,"full_ingredient_data":full_ingredient_data}
    context={"page":page,"id":id,"desc_full":desc_full,"title":content_json["_source"]["title"],"ingredient_data":ingredient_data,"simiarlity_kratoo":testdata}

    # print("pagedata",desc_full)


    stop = timeit.default_timer()

    print('Time: ', stop - start)  
    return render(request,'pagedata.html',context) 

def sendreport(request,id):
    messagedata=request.GET.get('message-text')
    print("messagedata",messagedata)
    try:
        report=Report()
        report.pantip_id=id
        report.report_data=messagedata
        report.save()

        messages.add_message(request, messages.INFO, 'Save Report')
    except:
        t, v, tb = sys.exc_info()
        messages.add_message(request, messages.ERROR, 'Error Save Report' )

    return HttpResponseRedirect(reverse('dashboard:pagedata',kwargs={'id':id}))


def searchmain(request):
    import timeit
    start = timeit.default_timer()
    page="dashboard"
    # testdata=[['37330463','https://ptcdn.info/images/unknown-avatar-38x38.png','น้ำพริกหนุ่ม ไข่ต้มยางมะตูม หมูสามชั้นทอด ผักต้ม',['a','b','c']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']],['37608989','https://f.ptcdn.info/308/057/000/p7v4ky7zidDPX02gSU1-o.jpg','ชวนทำเค้กลาวาสังขยาใบเตย สูตรจาก MasterChef Thailand',['ไข่ไก่','ไข่แดง','น้ำตาลปี๊บ','ใบเตยหอม']]]

    testdata=[]
    recipe_data = pantip_ingredients["recipe_data"]
    for i in recipe_data.find().sort("point",-1):
        testdata.append(i)
    notwant=request.GET.get('notwant')
    want=request.GET.get('want')
    searchinput=request.GET.get('searchinput')
    
    
    print("notwant",notwant)
    print("want",want)
    print("searchinput",searchinput)


    ingredient_dict = pantip_ingredients["ingredient_dict"]
    for i in ingredient_dict.find().sort("$natural", -1).limit(1):
        ingredient_dict_data=i

        ingredient_dict_data.pop("_id")
        ingredient_dict_data.pop("timestamp")
    category=[]
    allingredientlist=[]
    for key in ingredient_dict_data:
        category.append(key)
        for i in ingredient_dict_data[key]:
            allingredientlist+=ingredient_dict_data[key][i]
    # print(category)
    # print(sorted(allingredientlist))
    # print(ingredient_dict_data)

    if searchinput is None:
        searchinput=""
    else :
        searchinputlist=searchinput.split(",")
        temp_data=[]
        for i in testdata:
           if all(ele in i["title"]+' '+str(i["ingredients"])+str(i["tags"]) for ele in searchinputlist):
               temp_data.append(i)
        testdata=temp_data




    if notwant is None or notwant==[] or notwant=="[]" or notwant=='':
        notwant=[]

    else :
        if notwant[0]=='[':
            import ast
            notwant = ast.literal_eval(notwant) 
        else:
            notwant = notwant.split(',')  
        ############################    
        fullnotwant=[]

        for i in notwant:
            if i in ingredient_dict_data.keys():
                for j in ingredient_dict_data[i]:
                    fullnotwant+=ingredient_dict_data[i][j]
            else:
                # b=0
                for j in  ingredient_dict_data:
                    # if b == 1:
                    #     break
                    for k in ingredient_dict_data[j]:
                        if i in ingredient_dict_data[j][k]:
                            fullnotwant+=ingredient_dict_data[j][k]
                            # b =1
                            # break

        # notwant=fullnotwant

        temp_data=[]
        for i in testdata:
            if not any(ele in i["ingredients"] for ele in fullnotwant):
                temp_data.append(i)
        testdata=temp_data

    # a = [3, 45, 7, 2]
    # b = [2, 54, 13, 15]
    # cos_sim = dot(a, b)/(norm(a)*norm(b))
    # print("cos_sim",cos_sim)

    if want is None or want==[] or want=="[]" or want=='':
        want=[]
    else :
        if want[0]=='[':
            import ast
            want = ast.literal_eval(want) 
            want = list(set(want))

            
            
        else:
            want = want.split(',')
            want = list(set(want))
            print(want)
############################    
        fullwant=[]
        for i in want:
            if i in ingredient_dict_data.keys():
                for j in ingredient_dict_data[i]:
                    fullwant+=ingredient_dict_data[i][j]
            else:
                # b =0
                for j in  ingredient_dict_data:
                    # if b == 1:
                    #     break
                    for k in ingredient_dict_data[j]:
                        if i in ingredient_dict_data[j][k]:
                            fullwant+=ingredient_dict_data[j][k]
                            # b =1
                            # break
        # notwant=fullnotwant


        temp_data=[]
        for i in testdata:
            a=[1] * len(i["ingredients"])
            b=[]
            for j in i["ingredients"]:
                # print(j)
                if j in fullwant:
                    b.append(1)
                else:
                    b.append(0)
            cos_sim = dot(a, b)/(norm(a)*norm(b))
            if not isnan(cos_sim):
                # print(cos_sim)
                temp_data.append({"cos_sim":cos_sim,"data":i})
        temp_data=sorted(temp_data, key = lambda i: i['cos_sim'],reverse=True)
        
        temp_data=[x["data"] for x in temp_data] 
        # print(temp_data)
        testdata=temp_data

    


    

    

    context={"page":page,"searchdata":testdata,"searchinput":searchinput,"notwant":notwant,"want":want,"ingredientlist":sorted(allingredientlist),"category":category}


    stop = timeit.default_timer()

    print('Time: ', stop - start)  
    return render(request,'searchpage2.html',context) 


def downloadIngrediwnDict(request):
    ingredient_dict = pantip_ingredients["ingredient_dict"]
    for i in ingredient_dict.find().sort("$natural", -1).limit(1):
        ingredient_dict_data=i
        ingredient_dict_data.pop("_id")
        ingredient_dict_data.pop("timestamp")
    filepath=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'error/ingredient2.json')

    print(os.path.dirname(filepath), os.path.basename(filepath))
    
    with open('error/ingredient2.json', 'w', encoding='utf-8') as f:
        json.dump(ingredient_dict_data, f, ensure_ascii=False, indent=4)
    return serve(request, os.path.basename(filepath),os.path.dirname(filepath))
    
