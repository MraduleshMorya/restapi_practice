from django.contrib import admin
from django.urls import path,include
from serializer_app import views
from rest_framework.urlpatterns import format_suffix_patterns
from serializer_app import urls


urlpatterns = [
    path('details/', views.details),
    path('details/<str:input_username>/', views.employee_detail),
    
    path('snippets/', views.employee_list),
    path('snippets/<str:input_username>/', views.employee_detail),
    
    path('list/', views.Employee2List.as_view()),
    path('detail/<str:input_username>/', views.Employee2Detail.as_view()),
    
    path("login/", views.user_login, name="user_login"),
    path("userinfo/",views.user_info,name="user_info"),
    
    path('create_user/', views.create_user.as_view()),
    path('set_user/<str:id>/',views.set_user.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)