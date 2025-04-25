from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('export_selected/', views.export_selected_channel, name='export_selected_channel'),
    path('query/', views.sql_query_view, name='sql_query'),
    

]
