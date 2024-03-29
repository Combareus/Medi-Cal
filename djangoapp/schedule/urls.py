from django.urls import path #importing the path functions
from . import views #import view functions from current folder

#url configuration
urlpatterns = [
    path('', views.masterschedule, name='test'),
    path('test/', views.index, name='index'), #url path objects that receives the url, calls the function
    # path('login/', views.login, name='schedule-login'),
    # path('signup/', views.signup, name='schedule-signup')
    path('appointment/', views.appointment, name='appointment'),
    path('personschedule/', views.personschedule, name='personschedule')
]
