from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

#  This is the view for the index page

@login_required
def index(request):
    return render(request, 'index.html')

#  This is the view for the login page


def user_login(request):
    #  This is the if statement that checks if the request method is POST
    if request.method == 'POST':
        #  This is the username and password that is gotten from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
    # This is the authenticate function that checks if the user exists
        user = authenticate(request, username=username, password=password)
        #  This is the if statement that checks if the user is not None
        if user is not None:
            #  This is the login function that logs in the user
            login(request, user)
            #
            return redirect('/')
        else:
            error_message = 'Invalid credentials'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

#  This is the view for the signup page


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        print(username, email, password, repeat_password)
        if password == repeat_password:
            if User.objects.filter(username=username).exists():
                error_message = 'Username already exists'
                return render(request, 'signup.html', {'error_message': error_message})
            elif User.objects.filter(email=email).exists():
                error_message = 'Email already exists'
                return render(request, 'signup.html', {'error_message': error_message})
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                #  This is the login function that logs in the user after signing up successfully
                login(request, user)
                #  This is the redirect function that redirects the user to the index page after signing up successfully
                return redirect('/')
        else:
            error_message = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error_message})
        return render(request, 'login.html')
    return render(request, 'signup.html')

#  This is the view for the logout page


def user_logout(request):
    logout(request)
    return redirect('/')
