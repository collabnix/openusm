from django.shortcuts import render
import datetime
import json
import os
from django.shortcuts import render_to_response, render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf# Create your views here.
from django.contrib import auth
from django.utils.encoding import smart_unicode
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from django.templatetags.static import static

from redfish.models import Server

import operations


# Create your views here.

# Create your views here.
from django.http import HttpResponse
from redfish.operations import powerOn, resetServer, systemDetails,\
    importSCPServer, getBiosTokens, generateXML


def index(request):
    return HttpResponse("Hello World you are at the Index")

def login(request):
    c={}
    c.update(csrf(request))
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        if username =='admin' and password == 'admin':
            return redirect('/redfish/servers/')
        else:
            return redirect('/redfish/login/')
    
    
    
    return render(request,'login/login.html',c)

def servers(request):
    c={}
    c.update(csrf(request))
    return render(request,'servers/server_list.html',c)

def test(request):
    c={}
    c.update(csrf(request))
    return render(request,'servers/upload.html',c)

def upload_process(request):
    c={}
    c.update(csrf(request))
    return render(request,'servers/upload.html',c)

def pjm_index(request):
    print "h"
    return render(request,"pjm/pjm_index.html")

def insertServer(request):
    
    if request.method == 'POST':
        ip = request.POST['ip']
        username = request.POST['username']
        password = request.POST['password']
        
        print ip, username, password
        
        server = Server(ip=ip,username=username,password=password)
        server.save()
        
        return redirect('/redfish/servers/')
    print 'inside'    
    return render(request,'servers/servers_insert.html')

def deleteServer(request,server_id):
        
        gen = Server.objects.get(pk=server_id)
        gen.delete()
        return redirect('/redfish/servers/')

def updateServer(request,server_id):
    
    if request.method == 'POST':
        ip = request.POST['ip']
        username = request.POST['username']
        password = request.POST['password']
        
        
        server = Server.objects.get(pk=server_id)
        server.ip = ip
        server.username = username
        server.password = password
        
        server.save()
        
        return redirect('/redfish/servers/')
    
    server = Server.objects.get(pk=server_id)
    context = RequestContext(request)
    context_dict = {'server':server}
    response = render_to_response('servers/servers_update.html',context_dict,context)
    
    return response

def listServer(request):
    server_all = Server.objects.all()
   
    context = RequestContext(request)
    context_dict = {'serverlist':server_all }
    response = render_to_response('servers/servers_list.html',context_dict,context)  
    return response



#operations

def poweron(request,server_id):
      
    server = Server.objects.get(pk=server_id)
    print server.ip,server.username,server.password
    response = powerOn(server)
    print response 
    
    return redirect('/redfish/servers/')

def details(request,server_id):
    server = Server.objects.get(pk=server_id)
    print server.ip,server.username,server.password
    response = systemDetails(server)
    print response 
    
    return redirect('/redfish/servers/')

def reset(request,server_id):
    
    server = Server.objects.get(pk=server_id)
    print server.ip,server.username,server.password
    response = resetServer(server)
    print response
    
    return redirect('/redfish/servers/')
    
def importscp(request,server_id):
    server = Server.objects.get(pk=server_id)
    print server.ip,server.username,server.password
    response = importSCPServer(server)
    print response
    return redirect('/redfish/servers/')
    
def getServerDetails(request,server_id):
    context = RequestContext(request)
    server = Server.objects.get(pk=server_id)
    print server.ip,server.username,server.password
    
    outputdata = systemDetails(server)
    
    biosdata = getBiosTokens(server)
    
#     print biosdata
    
    context_dict = {'outputdata':outputdata,'server':server,'biosdata':biosdata}
    
    
    
    response = render_to_response('servers/bios_change.html',context_dict,context)
    return response

def bios_process(request,server_id):
    
    biosSettings = {}
    
    if request.method == 'POST':
        biosSettings['LogicalProc'] = request.POST['logicalproc'] 
        biosSettings['ProcVirtualization'] = request.POST['procvirtualization']
        biosSettings['ControlledTurbo'] = request.POST['controlledturbo'] 
        
        
        generateXML(biosSettings)
        
        
        
        
        
        return redirect('/redfish/servers/')
    
    return redirect('/redfish/servers/details/'+server_id)
