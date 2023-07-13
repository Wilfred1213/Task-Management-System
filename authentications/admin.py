from django.contrib import admin
from authentications.models import CustomUser, CompanyModel, ChooseGroup

admin.site.register(CustomUser)
admin.site.register(CompanyModel)
admin.site.register(ChooseGroup)
