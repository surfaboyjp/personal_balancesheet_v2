from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Journal)
admin.site.register(JournalRecord)
admin.site.register(Asset)
admin.site.register(Liability)
admin.site.register(Income)
admin.site.register(Cost)