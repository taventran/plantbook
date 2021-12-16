from django.contrib import admin
from . models import Plant, UserProfile, Follow

# Register your models here.
admin.site.register(Plant)
admin.site.register(UserProfile)
admin.site.register(Follow)
