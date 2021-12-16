from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import Transpose, Thumbnail, ResizeToFit, ResizeToFill



class UserProfile(models.Model):
	''' This model is for getting an avatar and a bio for users profile page. '''
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length = 50, blank=False, default="No bio")
	avatar = models.ImageField(default="images/Fat_Yoshi.png", upload_to='avatar')
	avatarFlip = ImageSpecField(source='avatar', processors=[
															Transpose(),
															ResizeToFill(200, 200),
															],
															format='JPEG',
															options={'quality':70})

	def __str__(self):
		return (f'{self.user.username} Profile')




class Follow(models.Model):
	''' Model to collect followers and who the user is following '''
	user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
	following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, blank=False)
	picture = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, default=1)

	def following(self):
		return (f"{self.following_user_id}")

	def __str__(self):
		return (f"{self.following_user_id}")


# Post model
class Plant(models.Model):
	''' Model for what data all of the posts will need to have '''
	date = models.DateTimeField(auto_now_add=True, blank=False)
	caption = models.CharField(max_length = 36, blank=True)
	photo = models.ImageField(upload_to='postImg', null=False, blank=False)
	photoFlip = ImageSpecField(source='photo', processors=[
																Transpose(),
																ResizeToFill(450, 400),
																],
																format='JPEG',
																options={'quality':70})
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	picture = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
	likes = models.ManyToManyField(User, related_name="plant_post")


	
	def check_if_liked(self):
		return self.likes.values_list('id', flat=True)

	def __str__(self):
		return f"{self.caption[:10]}"


