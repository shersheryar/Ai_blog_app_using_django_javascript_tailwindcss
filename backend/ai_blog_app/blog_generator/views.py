from django.shortcuts import render

# Create your views here.

#  This is the view for the index page


def index(request):
    return render(request, 'index.html')

#  This is the view for the login page


def user_login(request):
    return render(request, 'login.html')

#  This is the view for the signup page


def user_signup(request):
    return render(request, 'signup.html')

#  This is the view for the logout page


def user_logout(request):
     
    return render(request, 'logout.html')
