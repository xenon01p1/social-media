from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from authentication.models import CustomUser
from authentication.views import login
from my_profile.models import Followers
from explore.models import Posts
from home.models import Story, Seen_Story
from django.utils import timezone


def home(request):

    if 'user_email' not in request.session:
        return login(request)
    
    user_email = request.session.get('user_email')
    user_id = CustomUser.objects.get(email=user_email).id
    get_user_following = Followers.objects.filter(is_following=user_id).values_list('user_id', flat=True)
    following_posts = Posts.objects.filter(insert_by_id__in=get_user_following)
    followers = Followers.objects.filter(is_following=user_id)
    who_to_follow = CustomUser.objects.exclude(id=user_id)[:5]
    stories = Story.objects.all()
    
    follower_stories = {}
    seen_stories = set(Seen_Story.objects.filter(seen_by_id=user_id).values_list('story_id', flat=True))
    # get semua data seen_story yang dilihat oleh user_id
    # nanti di template akan di cek, apakah story id ada di data ini.

    for follower in followers:
        latest_story = Story.objects.filter(insert_by=follower.user_id).order_by('-id').first()
        if latest_story and timezone.now() < latest_story.delete_datetime:
            follower_stories[follower.user_id] = latest_story
            print(follower_stories.keys())

    context = {
        "followers": followers,
        "follower_post_stories": follower_stories.keys(),  
        "who_to_follow": who_to_follow,
        "posts": following_posts,
        "follower_stories": follower_stories,
        "seen_stories": seen_stories,  # Pass seen stories to the template
        "stories": stories
    }

    return render(request, "home/home.html", context)





