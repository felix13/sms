from django.urls import path

from . import views

app_name = "smsapp"


urlpatterns = [
    path('create_sms/', views.create_sms, name="create_sms"),
    path('incoming_message', views.incoming_message, name='incoming_message'),
    path('incoming_delivery_reports', views.incoming_delivery_reports, name='incoming_delivery_reports'),  
    path('delivery_reports', views.delivery_reports, name='delivery_reports'),
    path('inbox', views.inbox, name='inbox'),
]
