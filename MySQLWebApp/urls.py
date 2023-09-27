from django.urls import path
from . import views

urlpatterns = [
    path('', views.database_connection, name='database_connection'),
    path('execute_query/', views.execute_query, name='execute_query'),
]