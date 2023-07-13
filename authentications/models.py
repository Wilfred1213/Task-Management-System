from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class CompanyModel(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    moto = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank = True, null = True)
    image = models.ImageField(upload_to='media', null = True, blank=True)
    def __str__(self):
        return self.name
    
class ChooseGroup(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank = True, null = True)
    group = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, blank=False)
    
    def __str__(self):
        return self.group.name
    
class CustomUser(AbstractUser):
    is_personal = models.BooleanField('For personal use', default = False )
    is_group_leader = models.BooleanField('Group Leader', default = False )
    is_group_member=models.BooleanField('Group Member', default = False )
    group = models.ForeignKey(CompanyModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta(AbstractUser.Meta):
        swappable = 'authentications.CustomUser'
    
        # app_label = 'authentications'
    
    def __str__(self):
        return self.username
    

CustomUser.groups.field.remote_field.related_name = 'customuser_set'
CustomUser.user_permissions.field.remote_field.related_name = 'customuser_permissions_set'
# PersonalUser.groups.field.remote_field.related_name = 'personaluser_set'
# PersonalUser.user_permissions.field.remote_field.related_name = 'personaluser_permissions_set'