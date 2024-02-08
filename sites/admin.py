from django.contrib import admin
from .models import Site, Collector, Contact

admin.site.register(Site)
admin.site.register(Collector)
admin.site.register(Contact)