from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signup(request):
    if request.user.is_authenticated:
        return redirect('questions')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            new_user = form.save()
            new_user = authenticate(username=username,password=password1,)
            login(request, new_user)
            messages.info(request, "Thanks for registering. You are now logged in.")
            return redirect("questions")
        else:
            messages.error(request, 'Please provide valid credentials')
            return redirect('signup')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('questions')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Welcome ' + username)
            return redirect('questions')
        else:
            messages.error(request, 'Please provide valid credentials')
            
    form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)



def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('login')
