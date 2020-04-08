from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('details/',views.user_detail,name='user_detail'),
     path('login/',views.login,name='login'),
      path('access/',views.access,name='access'),
      path('register/',views.register,name='register'),
      path('insert_data/',views.insert_data,name='insert_data'),
      path('logout/',views.denied,name="denied"),
]
