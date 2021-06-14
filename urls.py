"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_crop_type_add', views.admin_crop_type_add, name='admin_crop_type_add'),
    path('admin_crop_type_edit', views.admin_crop_type_edit, name='admin_crop_type_edit'),
    path('admin_crop_type_view', views.admin_crop_type_view, name='admin_crop_type_view'),
    path('admin_crop_type_delete', views.admin_crop_type_delete, name='admin_crop_type_delete'),

    path('admin_expert_details_add', views.admin_expert_details_add, name='admin_expert_details_add'),
    path('admin_expert_details_edit', views.admin_expert_details_edit, name='admin_expert_details_edit'),
    path('admin_expert_details_view', views.admin_expert_details_view, name='admin_expert_details_view'),
    path('admin_expert_details_delete', views.admin_expert_details_delete, name='admin_expert_details_delete'),

    path('admin_user_details_view', views.admin_user_details_view, name='admin_user_details_view'),
    path('admin_user_details_delete', views.admin_user_details_delete, name='admin_user_details_delete'),


    path('admin_crop_master_view', views.admin_crop_master_view,name='admin_crop_master_view'),

    path('admin_seller_details_add', views.admin_seller_details_add, name='admin_seller_details_add'),
    path('admin_seller_details_view', views.admin_seller_details_view, name='admin_seller_details_view'),
    path('admin_seller_details_edit', views.admin_seller_details_edit, name='admin_seller_details_edit'),
    path('admin_seller_details_delete', views.admin_seller_details_delete, name='admin_seller_details_delete'),

    path('expert_login', views.expert_login, name='expert_login'),
    path('expert_changepassword', views.expert_changepassword, name='expert_changepassword'),
    path('expert_logout', views.expert_logout, name='expert_logout'),
    path('expert_home', views.expert_home, name='expert_home'),

    path('expert_crop_master_add', views.expert_crop_master_add,name='expert_crop_master_add'),
    path('expert_crop_master_edit', views.expert_crop_master_edit,name='expert_crop_master_edit'),
    path('expert_crop_master_view', views.expert_crop_master_view,name='expert_crop_master_view'),
    path('expert_crop_master_delete', views.expert_crop_master_delete,name='expert_crop_master_delete'),

    path('expert_crop_pics_add', views.expert_crop_pics_add, name='expert_crop_pics_add'),
    path('expert_crop_pics_delete', views.expert_crop_pics_delete, name='expert_crop_pics_delete'),
    path('expert_crop_pics_view', views.expert_crop_pics_view, name='expert_crop_pics_view'),

    path('expert_crop_variety_add', views.expert_crop_variety_add, name='expert_crop_variety_add'),
    path('expert_crop_variety_delete', views.expert_crop_variety_delete, name='expert_crop_variety_delete'),
    path('expert_crop_variety_view', views.expert_crop_variety_view, name='expert_crop_variety_view'),

    path('expert_crop_cultivation_add', views.expert_crop_cultivation_add, name='expert_crop_cultivation_add'),
    path('expert_crop_cultivation_delete', views.expert_crop_cultivation_delete, name='expert_crop_cultivation_delete'),
    path('expert_crop_cultivation_view', views.expert_crop_cultivation_view, name='expert_crop_cultivation_view'),

    path('expert_crop_fertilizer_add', views.expert_crop_fertilizer_add, name='expert_crop_fertilizer_add'),
    path('expert_crop_fertilizer_delete', views.expert_crop_fertilizer_delete, name='expert_crop_fertilizer_delete'),
    path('expert_crop_fertilizer_view', views.expert_crop_fertilizer_view, name='expert_crop_fertilizer_view'),

    path('expert_crop_pesticides_add', views.expert_crop_pesticides_add, name='expert_crop_pesticides_add'),
    path('expert_crop_pesticides_delete', views.expert_crop_pesticides_delete, name='expert_crop_pesticides_delete'),
    path('expert_crop_pesticides_view', views.expert_crop_pesticides_view, name='expert_crop_pesticides_view'),

    path('expert_crop_disease_add', views.expert_crop_disease_add, name='expert_crop_disease_add'),
    path('expert_crop_disease_delete', views.expert_crop_disease_delete, name='expert_crop_disease_delete'),
    path('expert_crop_disease_view', views.expert_crop_disease_view, name='expert_crop_disease_view'),

    path('expert_ask_expert_reply', views.expert_ask_expert_reply, name='expert_ask_expert_reply'),
    path('expert_ask_expert_view', views.expert_ask_expert_view, name='expert_ask_expert_view'),


    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('user_crop_master_search', views.user_crop_master_search, name='user_crop_master_search'),
    path('user_crop_master_view', views.user_crop_master_view, name='user_crop_master_view'),
    path('user_crop_pics_view', views.user_crop_pics_view, name='user_crop_pics_view'),
    path('user_crop_disease_view', views.user_crop_disease_view, name='user_crop_disease_view'),
    path('user_crop_cultivation_view', views.user_crop_cultivation_view, name='user_crop_cultivation_view'),
    path('user_crop_fertilizer_view', views.user_crop_fertilizer_view, name='user_crop_fertilizer_view'),
    path('user_crop_pesticides_view', views.user_crop_pesticides_view, name='user_crop_pesticides_view'),
    path('user_crop_variety_view', views.user_crop_variety_view, name='user_crop_variety_view'),

    path('user_expert_details_view', views.user_expert_details_view, name='user_expert_details_view'),

    path('user_ask_expert_add',views.user_ask_expert_add,name='user_ask_expert_add'),
    path('user_ask_expert_delete', views.user_ask_expert_delete, name='user_ask_expert_delete'),
    path('user_ask_expert_view', views.user_ask_expert_view, name='user_ask_expert_view'),
    path('user_product_view', views.user_product_view, name='user_product_view'),

    path('user_transaction_add', views.user_transaction_add, name='user_transaction_add'),
    path('user_transaction_view', views.user_transaction_view, name='user_transaction_view'),

    path('seller_home', views.seller_home, name='seller_home'),
    path('seller_login', views.seller_login, name='seller_login'),
    path('seller_changepassword', views.seller_changepassword, name='seller_changepassword'),
    path('seller_logout', views.seller_logout, name='seller_logout'),
    path('seller_product_details_add', views.seller_product_details_add, name='seller_product_details_add'),
    path('seller_product_details_view', views.seller_product_details_view, name='seller_product_details_view'),
    path('seller_transaction_view', views.seller_transaction_view, name='seller_transaction_view'),

    path('export_pdf', views.export_pdf, name='export_pdf'),
    path('export_pdf_invoice', views.export_pdf_invoice, name='export_pdf_invoice'),
    path('export_pdf_seller', views.export_pdf_seller, name='export_pdf_seller'),
]
