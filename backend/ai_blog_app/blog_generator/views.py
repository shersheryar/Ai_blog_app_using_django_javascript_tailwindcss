import yt_dlp
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
from pytube.exceptions import PytubeError
from .models import BlogPost


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
    try:
        video = YouTube(link)
        # Extract title from watch_html directly
        title = video.watch_html.split('<title>')[1].split('</title>')[0]
        title = title.replace(" - YouTube", "").strip()
        return title
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# ======================getting transcript file of the youtube video==================


def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        # Save to MEDIA_ROOT
        'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)  # Download the audio
            file_name = f"{info['title']}.mp3"  # Construct the file name
            # Full path to the file
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            return file_name, file_path  # Return file name and path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None  # Return None if an error occurs


# Example usage
# Replace with desired video link


def get_transcript(link):
    audio_file = download_audio(link)
    aai.settings.api_key = "37627fdab64a4848b60a2a53cfad31f7"
    transcriber = aai.Transcriber()
    # print("audio file", audio_file)
    transcript = transcriber.transcribe("https://assembly.ai/wildfires.mp3")
    if not transcript:
        return JsonResponse({'error': 'Transcription failed'}, status=500)

    return transcript.text


# =============================Generate blog from transcription=========================
# 
def generate_blog_from_transcription(transcription):

    openai.api_key = "write ur own"

    messages = [
        {"role": "user", "content": f"Based on the following transcript from a YouTube video, write a comprehensive blog article. Write it based on the transcript, but don't make it look like a YouTube video; make it look like a proper blog article: \n\n{transcription}\n\nArticle:"}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # Ensure you're using the correct model name
        messages=messages,
        max_tokens=1000
    )
    print("response", response)
    return response.choices[0].text.strip()
    # =============================blog generation view===============================================
    #  This is the view for the blog generation page


@ csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        # return JsonResponse({'content': yt_link})

        # if not yt_link:
        #     return JsonResponse({'error': 'No YouTube link provided'}, status=400)
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data send'}, status=400)

        # code for getting the title of the youtube video
        # get title of the video

        title = yt_title(yt_link)

        # get the transcript
        transcript = get_transcript(yt_link)
        if not transcript:
            return JsonResponse({'error': 'invalid response'}, status=400)

        # use openai  to generate the blog
        blog = generate_blog_from_transcription(transcript)
        if not blog:
            return JsonResponse({'error': 'failed to generate blog article'}, status=500)
        #  save the blog to the database
        new_blog_article = BlogPost.objects.create(
            # Save the blog to the database
            user=request.user, youtube_title=title, youtube_link=yt_link, generated_blog=blog)
        new_blog_article.save()
        # return the blog as a response
        return JsonResponse({'content': blog})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    # return render(request, 'generate_blog.html')

    # ================================================================================================


#  This is the view for the blog list page
def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, 'all-blogs.html', {'blog_articles': blog_articles})


# this is the view for blog-details
def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog-details.html', {'blog_article_detail': blog_article_detail})
    else:
        redirect('/')
