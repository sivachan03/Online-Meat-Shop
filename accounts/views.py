from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but don't save it yet
            new_user = user_form.save(commit=False)
            # Save the User object
            new_user.save()
            # Check if the user already has a profile
            if not hasattr(new_user, 'profile'):
                Profile.objects.create(user=new_user)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
        
        profile_form = ProfileEditForm(instance=profile, data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        try:
            profile_form = ProfileEditForm(instance=request.user.profile)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
            profile_form = ProfileEditForm(instance=profile)
    
    return render(request, 'accounts/edit.html', {'user_form': user_form, 'profile_form': profile_form})
