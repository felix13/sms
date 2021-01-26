from django.contrib import admin
from .models import Outbox, Inbox, DeliveryReport


admin.site.register(Outbox)
admin.site.register(Inbox)
admin.site.register(DeliveryReport)
