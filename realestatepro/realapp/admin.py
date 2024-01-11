from django.contrib import admin
from .models import Property,Tenant,Unit,RentalInformation


admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(Unit)
admin.site.register(RentalInformation)