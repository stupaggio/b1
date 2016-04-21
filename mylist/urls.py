from django.conf.urls import url, include, patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start_page/$', views.start_page, name='start_page'),
    url(r'^issues_to_fix/$', views.issues_to_fix, name='issues_to_fix'),
    url(r'show_user_subs_list/$', views.show_user_subs_list, name ='show_user_subs_list'),
    url(r'show_all_lists/$', views.show_all_lists, name = 'show_all_lists'),
    url(r'show_all_sublists/$', views.show_all_sublists, name = 'show_all_sublists'),
    url(r'show_subscribers_for_all_lists/$', views.show_subscribers_for_all_lists, name = 'show_subscribers_for_all_lists'),
    url(r'^checklist_detail/(?P<pk>\d+)/item/$', views.checklist_detail, name='checklist_detail'),
    url(r'^checklist_mkr/$', views.checklist_mkr, name='checklist_mkr'),
    url(r'^checklist_subd/$', views.checklist_subd, name='checklist_subd'),
    #url(r'show_list_items/(?P<pk>[0-9]+)/$',views.show_list_items, name = 'show_list_items'),
    url(r'list/new/$', views.list_new, name='list_new'),
    
    url(r'item/new/$', views.add_item_to_list, name='add_item_to_list'),
    
    url(r'^checklist/(?P<pk>[0-9]+)/item/$', views.add_item_to_checklist, name='add_item_to_checklist'),
    
    url(r'^list/(?P<pk>\d+)/add_item_to_list/$', views.add_item_to_list, name='add_item_to_list'),
    url(r'^list/(?P<pk>\d+)/subscribe/$', views.subscribe, name = 'subscribe'),
    url(r'^list/(?P<pk>\d+)/is_user_subscribed/$', views.is_user_subscribed, name = 'is_user_subscribed'),
    url(r'^list/(?P<pk>\d+)/un_subscribe/$', views.un_subscribe, name = 'un_subscribe'),
    
    url(r'^checklist/(?P<pk>[0-9]+)/remove/$', views.checklist_remove, name='checklist_remove'),
    url(r'^item/(?P<pk>[0-9]+)/remove/$', views.item_remove, name='item_remove'),
    url(r'^item/(?P<pk>[0-9]+)/purchased/$', views.item_purchased, name='item_purchased'),
    url(r'^checklist/(?P<pk>\d+)/confirm_list_code/$', views.confirm_list_code, name='confirm_list_code'),
    
  #url(r'^comment/(?P<pk>[0-9]+)/approve/$',views.comment_approve, name='comment_approve'),
    #search function..
    url(r'^search_for_lists/$', views.search_for_lists, name='search_for_lists'),
   
    ]
    