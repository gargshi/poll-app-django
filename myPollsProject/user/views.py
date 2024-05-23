from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

def register(request):
	return render(request,'register.html')

def doRegister(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']
		email = request.POST['email']
		if password == confirm_password:
			user = User.objects.create_user(username=username,password=password,email=email)
			user.save()			
			return redirect('user_login')
	return render(request,'register.html')

def user_login(request):
	return render(request,'login.html')

def doLogin(request):
	# logic for user login through django auth system
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		print(username,password)
		try:
			user=authenticate(username=username,password=password)
		except Exception as e:
			print(e)
		print("user=",user)
		if user is not None:
			login(request,user)
			messages.info(request, 'hi '+username+', You are now logged in!')
			return redirect('listPolls')		
		else:
			print("invalid credentials or user is none")
	return render(request,'login.html')

def user_logout(request):
	logout(request)
	return redirect('user_login')