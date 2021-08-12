from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
	caption=models.CharField(max_length=1400,blank=True)
	data_posted=models.DateTimeField(default=timezone.now)
	author=models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='blogpost_like')
	def __str__(self):
		return self.caption
	def number_of_like(self):
		return self.likes.count()

class PostImage(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	post_image=models.ImageField(upload_to='post_images')

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	content = models.CharField(max_length=500, blank=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now)