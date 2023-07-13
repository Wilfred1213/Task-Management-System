from django.urls import path
from .  import views

app_name = 'authentications'
urlpatterns = [
   
#     path('projectform', views.projectform, name='projectform' ),
    path('register_user/', views.register_user, name='register_user' ),
    path('register_company/', views.register_company, name='register_company' ),
    path('choose_your_group/', views.choose_your_group, name='choose_your_group' ),
    path('signout/', views.signout, name='signout' ),
    # path('userchoice/', views.userchoice, name='userchoice' ),
    path('personal_user_instructions/', views.personal_user_instructions, name='personal_user_instructions' ),
    
    path('loggin', views.loggin, name='loggin' ),
    path('group_leader_instructions', views.group_leader_instructions, name='group_leader_instructions' ),
    path('group_member_instructions', views.group_member_instructions, name='group_member_instructions' ),
    path('editgroup/<int:group_id>/', views.editgroup, name='editgroup' ),    
    
]