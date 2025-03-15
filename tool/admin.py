from django.contrib import admin
from .models import UserProfile, TechStack, Job, Company, Application, Chat

admin.site.register(UserProfile)
admin.site.register(TechStack)
admin.site.register(Job)
admin.site.register(Company)
admin.site.register(Application)
