from . models import Plant, UserProfile
from django.forms import ModelForm

class PlantForm(ModelForm):
	class Meta:
		model = Plant
		fields = ['caption', 'photo']

class UserProfileUpdateForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['avatar', 'bio']
	

	