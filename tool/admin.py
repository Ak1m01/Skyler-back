from django.contrib import admin
from .models import UserProfile, TechStack, Vacancy, Company, Application, PrivateEmployer

admin.site.register(UserProfile)
admin.site.register(TechStack)
admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Application)
admin.site.register(PrivateEmployer)

