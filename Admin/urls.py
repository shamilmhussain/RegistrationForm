from django.urls import path
from . import views

urlpatterns = [
    path('',views.memberRegistrationView, name='registration'),
    path('login/',views.adminLoginView, name='login'),
    path('admin/',views.RegisteredView, name='registered'),
    path('view/<int:id>/',views.memberView, name='view'),
        
]
