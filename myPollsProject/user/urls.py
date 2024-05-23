from django.urls import path
from . import views

urlpatterns = [
	path('register/',views.register,name="user_register"),
	path('login/',views.user_login,name="user_login"),
	path('doRegister/',views.doRegister,name="user_doRegister"),
	path('doLogin/',views.doLogin,name="user_doLogin"),
	path('doLogout/',views.user_logout,name="user_doLogout"),
]