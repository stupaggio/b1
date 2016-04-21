from django.contrib import admin

# Register your models here.
from .models import Checklist
from .models import Sublist
from .models import Item

admin.site.register(Checklist)
admin.site.register(Sublist)
admin.site.register(Item)
