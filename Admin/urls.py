from django.urls import path
from . import views

urlpatterns = [
    path('',views.memberRegistrationView, name='registration'),
    path('login/',views.adminLoginView, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('admin/',views.RegisteredView, name='registered'),
    path('view/<int:id>/',views.memberView, name='view'),
    path('edit/<int:id>/',views.editMemberView, name='edit'),
    path('pdf/<int:id>/',views.memberPdfView, name='pdf'),
        
]
