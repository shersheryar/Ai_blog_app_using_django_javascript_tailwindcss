from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from pytube import YouTube
import assemblyai as aai
import openai
import json
import os


# Create your views here.
# =============================login, logut and signup views=============================
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
# ================================================================================================
 # ===================getting the titile of youtube video=========================


def yt_title(link):
    yt = YouTube(link)
    return yt.title
# ======================getting transcript file of the youtube video==================


def download_audio(link):
    yt = YouTube(link)
    audio = yt.streams.filter(only_audio=True).first()
    out_file = audio.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file


def get_transcript(link):
    audio_file = download_audio(link)
    # add your assemblyai api key
    aai.settings.api_key = " "
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    if not transcript:
        return JsonResponse({'error': 'Transcription failed'}, status=500)

    return transcript.text
# =============================Generate blog from transcription=========================


def generate_blog_from_transcription(transcript):
    pass
# =============================blog generation view===============================================
#  This is the view for the blog generation page


@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data['link']
            # print(yt_link)
            # return JsonResponse({'content': yt_link})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)

        # get title of the video
            title = yt_title(yt_link)
        # get the transcript
            transcript = get_transcript(yt_link)
        # use openai  to generate the blog

        #  save the blog to the database

        # return the blog as a response

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    # return render(request, 'generate_blog.html')


# ================================================================================================
