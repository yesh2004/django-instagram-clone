from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Message
from homepage.models import Post,PostImage
from django.urls import reverse
# Create your views here.
def register(request):
	if request.user.is_authenticated:
		return redirect('home_page')
	else:
		form=CreateUserForm()
		if request.method=='POST':
			form=CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('home_page')
		context={'form':form}
		return render(request,'register.html',context)

def login(request):
	
	if request.user.is_authenticated:
		return redirect('home_page')
	else:

		if request.method=='POST':
			username=request.POST.get('username')
			password=request.POST.get('password')
			
			user=authenticate(request,username=username,password=password)
			
			if user is not None:
				django_login(request,user)
				return redirect('home_page')
			else:
				messages.info(request, 'Username OR password is incorrect')
	context={}
	return render(request,'login.html',context)
@login_required(login_url='login_page')
def logout(request):
	django_logout(request)
	return redirect('login_page')
@login_required(login_url='login_page')
def profile(request):
	profile=Profile.objects.get(user=request.user)
	posts=Post.objects.filter(author=request.user)
	post_images=PostImage.objects.filter(post__author=request.user)
	for post in post_images:
		print(post.post_image)
	context={
	'profile':profile,
	'posts':posts,
	'post_images':post_images
	}
	return render(request,'profile.html',context)

@login_required(login_url='login_page')
def direct(request,username):
	users=User.objects.all()
	user=request.user
	send=username
	messages=Message.get_messages(user=user)
	directs=Message.objects.filter(sender__username=send,receiver__username=user)
	
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0
	for user in users:
		print(user,username)
		print(user==str(username))
	context={
	'users':users,
	'to_user':username,
	'messages':messages,
	'directs':directs
	}
	return render(request,'direct.html',context)

@login_required
def SendDirect(request):
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	content = request.POST.get('content')
	
	if request.method == 'POST':
		print(from_user,to_user_username,content)
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user, content)
		return redirect('direct_message',username=to_user_username)
	else:
		HttpResponseBadRequest()

	
	
