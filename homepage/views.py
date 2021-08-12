from django.shortcuts import render,redirect
from .forms import PostForm,ImageForm,CommentForm
from .models import PostImage,Post,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
@login_required(login_url='login_page')
def index(request):
	posts=PostImage.objects.all()
	form=CommentForm()
	comments=Comment.objects.all()

	
	context={
	'posts':posts,
	'form':form,
	'comments':comments
	
	}
	return render(request,'homepage.html',context)

@login_required(login_url='login_page')
def post(request):
	post_form=PostForm()
	image_form=ImageForm()
	if request.method=='POST':
		postform=PostForm(request.POST)
		imageform=ImageForm(request.POST,request.FILES)


		print(imageform.is_valid())
		if postform.is_valid() and imageform.is_valid():
			post=postform.save(commit=False)
			post.author=request.user
			post.save()

			image=imageform.cleaned_data['post_image']
			photo=PostImage(post=post,post_image=image)
			photo.save()
			messages.info(request, 'post created')
			return redirect('home_page')
		else:
			messages.info(request, 'post rror')
	context={
	'post_form':post_form,
	'image_form':image_form
	}
	return render(request,'post.html',context)
def postlike(request,pk):
	 post = get_object_or_404(Post, id=request.POST.get('post_id'))
	 if post.likes.filter(id=request.user.id).exists():
	 	post.likes.remove(request.user)
	 else:
	 	post.likes.add(request.user)
	 return HttpResponseRedirect(reverse('home_page'))

@login_required(login_url='login_page')
def comment(request,pk):
	if request.method=='POST':
		post=Post.objects.get(pk=pk)
		author=request.user
		form=CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author=author
			comment.post=post
			comment.save()
	return HttpResponseRedirect(reverse('home_page'))
	
