from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('projectform/', views.projectform, name='projectform' ),
    path('assigntask/<int:project_id>/', views.assigntask, name='assigntask' ),
    path('deletetask/<int:task_id>/', views.deletetask, name='deletetask' ),
    path('deleteproject/<int:project_id>/', views.deleteproject, name='deleteproject' ),
    path('viewtask/', views.viewtask, name='viewtask' ),
    path('groupdetail/<int:group_id>/', views.groupdetail, name='groupdetail' ),
    path('editproject/<int:project_id>/', views.editproject, name='editproject' ),

]