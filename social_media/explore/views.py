from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Posts, SearchLog
from home.models import Story, Seen_Story
from authentication.models import CustomUser
from authentication.views import login
from general_process.models import Likes, Comments, CategoryFavorites, Favorites
from django.utils.text import slugify
from django.utils import timezone
from django.http import HttpResponseNotFound
import os
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def explore(request):

    if 'user_email' not in request.session:
        return login(request)

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        user_email = request.session.get('user_email')
        user = CustomUser.objects.get(email=user_email)
        search_log_insert = SearchLog(keyword=keyword, user_id=user)
        search_log_insert.save()

        users_data = CustomUser.objects.filter(name__icontains=keyword)
        context = {
            "users": users_data
        }
        return render(request, "explore/search_user.html", context)

    posts = Posts.objects.all()
    context = {
        "posts": posts
    }
    return render(request, "explore/explore.html", context)



def scroll_post(request, id):

    if 'user_email' not in request.session:
        return login(request)
    
    try:
        id = int(id)  # Convert id to an integer
    except ValueError:
        # Handle the case where id is not a valid integer, for example, by returning a 404 response
        return HttpResponseNotFound("Invalid user profile")

    if request.method == 'POST':
        comment_content = request.POST.get('comment')

        current_url = reverse('explore:scroll_post', args=[id])

        # Redirect back to the current page after adding the comment
        comment_url = reverse('general_process:comment', args=[id, comment_content])
        return redirect(comment_url, comment_content=comment_content, next=current_url)

    post_info = Posts.objects.get(id=id)
    user_info = CustomUser.objects.get(id=post_info.insert_by.id)
    all_comments = Comments.objects.filter(posts_id=id)
    check_like = Likes.objects.filter(posts_id=post_info, liked_by=user_info).first()
    check_name = "heart" if check_like else "heart-outline"
    check_class = "text-danger" if check_like else ""
    check_bookmark = Favorites.objects.filter(posts_id=post_info, user_id=user_info)
    bookmark_icon = "bookmark" if check_bookmark else "bookmark-outline"

    context = {
        "post": post_info,
        "user": user_info,
        "check_name": check_name,
        "check_class": check_class,
        "bookmark_icon": bookmark_icon,
        "check_bookmark": check_bookmark,
        "comments": all_comments,
        
    }
    return render(request, "explore/scroll_post.html", context)


def category_favorite(request,id):

    if 'user_email' not in request.session:
        return login(request)
    
    user_email = request.session.get("user_email")
    user_id = CustomUser.objects.get(email=user_email)
    category_favorite = CategoryFavorites.objects.filter(user_id=user_id)
    
    context = {
        "category_favorite": category_favorite,
        "post_id": id
    }

    return render(request, "explore/category_favorite.html", context)


def category_unfavorite(request, id):

    if 'user_email' not in request.session:
        return login(request)
    
    user_email = request.session.get("user_email")
    user_id = CustomUser.objects.get(email=user_email)
    favorites = Favorites.objects.filter(user_id=user_id, posts_id=id)  

    for favorite in favorites:
        category = favorite.category_favorite_id 
        category.category_count -= 1
        category.save()
        favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))




def create_category_favorite(request):

    if 'user_email' not in request.session:
        return login(request)

    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = CustomUser.objects.get(email=user_email)
        category_name = request.POST.get('name')
        new_category = CategoryFavorites(name=category_name, category_count=0, user_id=user)
        new_category.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "explore/create_category_favorite.html")


def create_story(request):

    if 'user_email' not in request.session:
        return login(request)

    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user_id = CustomUser.objects.get(email=user_email)

        try:
            last_story = Story.objects.filter(insert_by=user_id).order_by('-id').first()
            if last_story and last_story.delete_datetime > timezone.now():
                context = {
                    'status': 'Exceeded post'
                }
                return render(request, "explore/create_story.html", context)
        except ObjectDoesNotExist:
            pass

        stories = request.FILES.getlist('files')
        delete_datetime = datetime.now() + timedelta(hours=24)

        new_story = Story(
            delete_datetime=delete_datetime,
            insert_by=user_id,
            delete_status=0
        )

        new_story.save()

        for i, image in enumerate(stories):
            filename, extension = os.path.splitext(image.name)
            new_filename = f"story_{timezone.now().strftime('%H_%M_%S')}_{filename}{extension}"
            setattr(new_story, f'file', new_filename)

            # Save the file to the media folder
            with open(os.path.join(settings.MEDIA_ROOT, new_filename), 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

        new_story.save()

        return redirect('/home/')

    return render(request, "explore/create_story.html")


def create_post(request):

    if 'user_email' not in request.session:
        return login(request)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        caption = request.POST.get('caption')
        post_images = request.FILES.getlist('files')
        user_email = request.session.get('user_email')
        user_id = CustomUser.objects.get(email=user_email).id

        new_post = Posts(
            name=name,
            caption=caption,
            like_count=0,
            comment_count=0,
            insert_by_id=user_id,
            delete_status=0
        )

        new_post.save()

        for i, image in enumerate(post_images):
            filename, extension = os.path.splitext(image.name)
            new_filename = f"file_{i + 1}_{timezone.now().strftime('%H_%M_%S')}_{filename}{extension}"
            setattr(new_post, f'file_{i + 1}', new_filename)

            # Save the file to the media folder
            with open(os.path.join(settings.MEDIA_ROOT, new_filename), 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

        new_post.save()

        return redirect('/explore/')

    return render(request, "explore/create.html")