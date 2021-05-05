"""Django01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('api/searchAll/', views.searchAll),
    path('', views.index),
    path('api/search/<str:name>/', views.searchNode),
    path('api/bridge/', views.showBridge),
    path('api/addRelationship/', views.addRelationship),
    path('api/addNode/<str:nodeType>/', views.addNode),
    path('api/reviseNode/<int:identity>/', views.reviseNode),
    path('api/deleteRe/<int:identity>/', views.deleteRelationship),
    path('api/deleteNL/<int:identity>/', views.deleteNodeAndLinks),
    path('api/showRelations/<int:identity>/<str:relationType>/', views.showRelations),
    path('api/showNodes/', views.test)
]
