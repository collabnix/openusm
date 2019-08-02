'''
Created on Jun 5, 2017

@author: Avinash_Bendigeri
'''
from django.conf.urls import patterns, url
from redfish import views



urlpatterns = patterns('',
                       url(r'^$', views.login),
                       url(r'^login/$', views.login),
                       
                       url(r'^add/$', views.test),
                       url(r'^upload_process/$', views.upload_process),
                       
                       url(r'pjm_index/$',views.pjm_index),
                       
                       url(r'servers/insert/$',views.insertServer,name='server.insert'),
                       url(r'servers/delete/(?P<server_id>\d+)$',views.deleteServer,name='server.delete'),
                       url(r'servers/update/(?P<server_id>\d+)$',views.updateServer,name='server.update'),
                       url(r'servers/$',views.listServer,name='server.get'),


                       url(r'servers/poweron/(?P<server_id>\d+)$',views.poweron,name='server.poweron'),
                       url(r'servers/reset/(?P<server_id>\d+)$',views.reset,name='server.reset'),
                       
                       url(r'servers/details/(?P<server_id>\d+)$',views.getServerDetails,name='server.details'),
                       
                       
                       url(r'servers/importscp/(?P<server_id>\d+)$',views.importscp,name='server.importscp'),
                       
                       url(r'servers/bios_process/(?P<server_id>\d+)$',views.bios_process,name='server.bios_process'),
                       
                       
                       
                       
   )

