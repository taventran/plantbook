from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from . models import Plant, UserProfile, Follow
from django.contrib.auth import logout
from django.contrib.auth.models import User
from . form import PlantForm, UserProfileUpdateForm
from django.urls import reverse 
from django.core.paginator import Paginator
from django.db.models import Q


def about(request):
	return render(request, 'plants/about.html')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'plants/register.html', {'form':form})

def logout_request(request):
	logout(request)
	return redirect('login')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request,"plants/login.html", {"form":form})


def likeView(request, pk):
	post = get_object_or_404(Plant, id=request.POST.get('plant_id'))
	liked = False
	if request.user.is_authenticated == False:
		messages.info(request, "Must login to like a post")
	elif post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	return redirect(request.META.get('HTTP_REFERER'))


def home(request):
	plant = Plant.objects.all().order_by('-date')
	plant_paginator = Paginator(plant, 3)
	page_num = request.GET.get('page')
	page = plant_paginator.get_page(page_num)


	return render(request, 'plants/home.html', {'page': page,})


def profile(request, id):
	currentUser = request.user
	page_user = User.objects.get(id=id)
	page_user_followers = len(Follow.objects.filter(following_user_id=page_user))
	page_user_following = len(Follow.objects.filter(user_id=page_user))
	user_followers = Follow.objects.filter(following_user_id=page_user)
	user_followers_list = []
	print(user_followers)
	for follower in user_followers:
		user_followers0 = follower.user_id
		print(user_followers0)
		user_followers_list.append(user_followers0)

	print(user_followers_list)
	profileBio = UserProfile.objects.get(user=id)
	plant = Plant.objects.filter(user=id).order_by('-date')
	plant_paginator = Paginator(plant, 3)
	page_num = request.GET.get('page')
	page = plant_paginator.get_page(page_num)

	if currentUser == page_user:
		return redirect('userProfile')
	elif currentUser.is_authenticated:
		if currentUser in user_followers_list:
			follow_button_value = 'unfollow'
		else:
			follow_button_value = 'follow'
		context = {
		'page': page, 
		'page_user': page_user, 
		'bio': profileBio,
		'followers': page_user_followers,
		'following': page_user_following,
		'follow_button_value': follow_button_value,
		}
		return render(request,'plants/profile.html', context)
	else:
		messages.info(request, "Must login to view profile page")
		return redirect('login')


def delete_post(request, post_id=None):
	post_to_delete = Plant.objects.get(id=post_id)
	post_to_delete.delete()
	return redirect('userProfile')


def userProfile(request):
	currentUser = request.user
	if currentUser.is_authenticated:
		page_user_followers = len(Follow.objects.filter(following_user_id=currentUser))
		page_user_following = len(Follow.objects.filter(user_id=currentUser))
		profileBio = UserProfile.objects.get(user=currentUser)
		plant = Plant.objects.filter(user=currentUser).order_by('-date')
		plant_paginator = Paginator(plant, 3)
		page_num = request.GET.get('page')
		page = plant_paginator.get_page(page_num)
		context = {
			'page': page, 
			'user': currentUser, 
			'bio': profileBio,
			'followers': page_user_followers,
			'following': page_user_following 
		}
		return render(request, 'plants/userprofile.html', context)
	else:
		messages.info(request, "Must login to view profile page")
		return redirect('login')


def followView(request, id):
	if request.method == "POST":
		user = request.POST['user']
		follower = request.POST['follower']
		value = request.POST['value']
		print(value)
		page_user = User.objects.get(username=user)
		currentUser = User.objects.get(username=follower)
		if value == 'follow':
			follower_cnt = Follow.objects.create(user_id=currentUser, following_user_id=page_user)
			follower_cnt.save()
			return redirect(request.META.get('HTTP_REFERER'))
		else:
			follower_cnt = Follow.objects.get(user_id=currentUser, following_user_id=page_user)
			follower_cnt.delete()
			return redirect(request.META.get('HTTP_REFERER'))
	return redirect('home')



def updateUserProfile(request):
	form = UserProfileUpdateForm(instance=request.user.userprofile)
	if request.method == "POST":
		form = UserProfileUpdateForm(request.POST, files=request.FILES, instance=request.user.userprofile)
		if form.is_valid():
			form.save()
			return redirect('userProfile')

	return render(request, 'plants/updateprofile.html', {'form':form})


def create_post(request, id):
	if request.method == "POST":
		form = PlantForm(request.POST, files=request.FILES)
		if form.is_valid():
			new_post = form.save(commit = False)
			new_post.user = request.user
			form.save()
			messages.success(request, f"New post created")
			return redirect('home')
	form = PlantForm()
	return render(request, 'plants/create.html', {'form':form})

def follows(request, user):
	getUser = User.objects.get(username=user)
	amount_of_followers = Follow.objects.filter(following_user_id=getUser.id)
	return render(request, 'plants/followers.html', {'followers': amount_of_followers})


def following(request, user):
	getUser = User.objects.get(username=user)
	amount_of_followers = Follow.objects.filter(user_id=getUser.id)
	
	return render(request, 'plants/followers.html', {'followings': amount_of_followers})

def personalizeFeed(request):
	currentUser = request.user
	following = Follow.objects.filter(user_id=currentUser.id).values('following_user_id')
	amount_of_following = len(Follow.objects.filter(user_id=currentUser.id))
	less_than_0 = True
	if amount_of_following > 0:
		less_than_0 = False
	print(following)
	plant = Plant.objects.filter(user__in=following).order_by('-date')
	print(plant)
	plant_paginator = Paginator(plant, 3)
	page_num = request.GET.get('page')
	page = plant_paginator.get_page(page_num)
	context = {'page': page, 'following':less_than_0}
	
	return render(request, 'plants/yourfeed.html', context)