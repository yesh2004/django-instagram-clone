from django import forms
from .models import Post,PostImage,Comment

class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=['caption']

class ImageForm(forms.ModelForm):
	class Meta:
		model=PostImage
		fields=['post_image',]

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=['content']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['content'].widget.attrs.update({'autofocus': 'autofocus', 'placeholder': 'Add a comment...'})