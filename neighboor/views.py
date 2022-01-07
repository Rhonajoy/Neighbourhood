from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from .models import Business, NeighbourHood, Post, Profile
from django.contrib.auth.decorators import login_required
from.forms import UpdateProfileForm,NeighbourhoodForm,PostForm,BusinessForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def home(request):
 return render(request,'index.html')
def neighborhood(request):
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighborhood = form.save(commit=False)
            neighborhood.admin = request.user.profile
            neighborhood.save()
            messages.success(request,'Neighborhood created successfully.')
            return redirect('neighborhood')
    else:
        form = NeighbourhoodForm()
        neighborhoods = NeighbourHood.objects.all()
        neighborhoods = neighborhoods[::-1]
    return render(request, 'profile.html', {'form': form, 'neighborhoods': neighborhoods})


def addpost(request):
 return render(request,'add_post.html')
def addbusiness(request):
 return render(request,'add_business.html')
def profile(request,user_id):

    current_user=get_object_or_404(User,id=user_id)
    # current_user = request.user
    
    profile = Profile.objects.filter(user = current_user.id).first()
    
    return render(request, 'profile/profile.html', {"profile": profile})
  
def update_profile(request):
  	#Get the profile
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    if request.method == 'POST':
        profileform = UpdateProfileForm(request.POST,request.FILES,instance=profile)
        if  profileform.is_valid:
            profileform.save(commit=False)
            profileform.user=request.user
            profileform.save()
            return redirect('profile')
    else:
        form=UpdateProfileForm()
    return render(request,'profile/update_profile.html',{'form':form})
@login_required
def neighborhood(request, neighborhood_id):
    neighborhood = NeighbourHood.objects.get(id=neighborhood_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        business_form = BusinessForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.neighborhood = neighborhood
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been added successfully.')
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.neighborhood = neighborhood
            business.user = request.user
            business.save()
            messages.success(request, 'Business added successfully.')
            return redirect('my_neighborhood', neighborhood_id)
    else:
        post_form = PostForm()
        business_form = BusinessForm()
        current_user = request.user
        neighborhood = NeighbourHood.objects.get(id=neighborhood_id)
        business = Business.objects.filter(neighborhood_id=neighborhood)
        users = Profile.objects.filter(neighborhood=neighborhood)
        posts = Post.objects.filter(neighborhood=neighborhood)
    return render(request, 'neighbourhood.html', {'post_form':post_form, 'business_form': business_form, 'users':users,'current_user':current_user, 'neighborhood':neighborhood,'business':business,'posts':posts})


