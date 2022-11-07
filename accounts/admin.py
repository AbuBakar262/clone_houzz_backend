from django.contrib import admin
from accounts.models import User, Projects, Company

# Register your models here.
admin.site.register(User)
admin.site.register(Projects)
admin.site.register(Company)