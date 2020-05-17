from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.MemberRegistration)
admin.site.register(models.RegisterErrorLog)
