from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.register, name='register'),
	path('', views.home, name='home'),
	path('login/', views.login_request, name='login'),
	path('logout/', views.logout_request, name='logout'),
	path('profile/<int:id>/',views.profile, name='profile'),
	path('yourprofile', views.userProfile, name='userProfile'),
	path('create/<int:id>', views.create_post, name='post'),
	path('update/', views.updateUserProfile, name='update'),
	path('like/<int:pk>', views.likeView, name='like_post'),
	path('delete/<post_id>', views.delete_post, name='delete'),
	path('about/', views.about, name="about"),
	path('follow/<int:id>', views.followView, name="follow_account"),
	path('follows/<str:user>', views.follows, name="follows"),
	path('following/<str:user>', views.following, name="following"),
	path('yourfeed/', views.personalizeFeed, name="feed")
]
