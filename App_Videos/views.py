from django.shortcuts import render, get_object_or_404
from App_Videos.models import Video, Category, Comment, Feedback
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def video_list(request):
    categories = Category.objects.all()
    category_videos = {category: Video.objects.filter(category=category) for category in categories}
    return render(request, 'App_Videos/video_list.html', {'category_videos': category_videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    comments = Comment.objects.filter(video=video)
    feedback = Feedback.objects.filter(video=video, user=request.user).first()

    # Extract YouTube video ID from the link
    youtube_video_id = get_youtube_video_id(video.youtube_link)

    return render(request, 'App_Videos/video_detail.html', {'video': video, 'comments': comments, 'feedback': feedback, 'youtube_video_id': youtube_video_id})

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    videos = Video.objects.filter(category=category)
    return render(request, 'App_Videos/category_detail.html', {'category': category, 'videos': videos})

@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    if request.method == 'POST':
        text = request.POST.get('comment_text', '')
        Comment.objects.create(video=video, user=request.user, text=text)

    return HttpResponseRedirect(reverse('App_Videos:video_detail', args=[video_id]))

@login_required
def add_feedback(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    like = request.GET.get('like')
    dislike = request.GET.get('dislike')

    if like:
        Feedback.objects.update_or_create(video=video, user=request.user, defaults={'like': True, 'dislike': False})
    elif dislike:
        Feedback.objects.update_or_create(video=video, user=request.user, defaults={'like': False, 'dislike': True})
    
    return HttpResponseRedirect(reverse('App_Videos:video_detail', args=[video_id]))

def get_youtube_video_id(youtube_link):
    # Extracts YouTube video ID from various YouTube video URL formats
    # Assumes that the link provided is a valid YouTube link

    video_id = None

    # Example YouTube video link formats:
    # - https://www.youtube.com/watch?v=VIDEO_ID
    # - https://youtu.be/VIDEO_ID
    # - https://www.youtube.com/embed/VIDEO_ID
    # - ... and others

    if 'youtube.com/watch?v=' in youtube_link:
        video_id = youtube_link.split('youtube.com/watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in youtube_link:
        video_id = youtube_link.split('youtu.be/')[1]
    elif 'youtube.com/embed/' in youtube_link:
        video_id = youtube_link.split('youtube.com/embed/')[1]

    return video_id
