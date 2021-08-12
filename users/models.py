from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.db.models import Max

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	bio = models.CharField(max_length=150, blank=True)

	@receiver(post_save, sender=User) #add this
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User) #add this
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
class Message(models.Model):
	sender = models.ForeignKey(User, related_name="senders", on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, related_name='receivers', on_delete=models.CASCADE)
	content = models.CharField(max_length=2200)
	date_created = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)
	def send_message(from_user, to_user, body):
		sender_message=Message(
			sender=from_user,
			receiver=to_user,
			content=body,
			is_read=True)
		sender_message.save()

		recipient_message = Message(
			
			sender=from_user,
			content=body,
			receiver=from_user,)
		recipient_message.save()
		return sender_message
	def get_messages(user):
		messages = Message.objects.filter(sender=user).values('receiver').annotate(last=Max('date_created')).order_by('-last')
		users = []
		for message in messages:
			users.append({
				'user': User.objects.get(pk=message['receiver']),
				'last': message['last'],
				'unread': Message.objects.filter(sender=user, receiver__pk=message['receiver'], is_read=False).count()
				})
		return users