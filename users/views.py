from django.shortcuts import render, redirect
# forms are classes that are generated from our models....classes get converted to html = forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateImgForm, ProfileUpdateAboutForm
from blog.models import Post
from .models import User

def register(request):
    if request.method== 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now log in as { username }')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html', {'form':form})

@login_required
def profile(request):
    if(request.method == 'POST'):
        u_form = UserUpdateForm(request.POST,instance=request.user)
        pi_form = ProfileUpdateImgForm(request.POST, #So that the user inputted stuff also is there
                                  request.FILES , # So tht the user uploaded  fike(image) is taken
                                  instance=request.user.profile)
        pa_form = ProfileUpdateAboutForm(request.POST, #So that the user inputted stuff also is there
                                  instance=request.user.profile)
        if u_form.is_valid() and pi_form.is_valid() and pa_form.is_valid():
            u_form.save()
            pi_form.save()
            pa_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-posts',request.user.username) #Redirecting should happen bcos of POST_GET_REDIRECT PATTERN
        # POST rquest made - then should be changed to GET request or else - if reloaded => again POST request
        # If we did not redirect, it would have gone to template directly at the end of else
    else:
        u_form = UserUpdateForm(instance=request.user)
        pi_form = ProfileUpdateImgForm(instance=request.user.profile) 
        pa_form = ProfileUpdateAboutForm(instance=request.user.profile) 
    return render(request,'users/profile.html',{'u_form' : u_form , 'pi_form' : pi_form, 'pa_form' : pa_form})