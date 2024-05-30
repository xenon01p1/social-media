from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from .models import Likes, Comments, Favorites, CategoryFavorites
from authentication.models import CustomUser
from authentication.views import login
from explore.models import Posts
from my_profile.models import Followers
from home.models import Seen_Story, Story
from django.shortcuts import get_object_or_404
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


# Create your views here.

def like(request, id):

    if 'user_email' not in request.session:
        return login(request)

    try:
        target_post = get_object_or_404(Posts, id=id)
        email = request.session.get('user_email')
        user = get_object_or_404(CustomUser, email=email)

        existing_like = Likes.objects.filter(posts_id=target_post, liked_by=user).first()

        if existing_like:
            # If there's an existing like, delete it and decrease like_count
            target_post.like_count -= 1
            target_post.save()

            existing_like.delete()

            return JsonResponse({'success': False})

        else:
            # If the user hasn't liked the post, add a new like and increase like_count
            target_post.like_count += 1
            target_post.save()

            new_like = Likes(posts_id=target_post, liked_by=user)
            new_like.save()

            print(existing_like)  # Check if an existing like is found
            print(target_post.like_count)

            return JsonResponse({'success': True})


    except Posts.DoesNotExist:

        logger.exception('Post does not exist')
        return JsonResponse({'success': False, 'error': 'Post does not exist'}, status=404)

    except Exception as e:

        logger.exception('Error processing like')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def follow(request, id):

    if 'user_email' not in request.session:
        return login(request)
    
    try:
        id = int(id)
        target_user = CustomUser.objects.get(id=id)
        email = request.session.get('user_email')
        user = CustomUser.objects.get(email=email)

        existing_follower = Followers.objects.filter(is_following=user.id, user_id=target_user.id).first()


        if existing_follower is not None:
            print(f"Before deletion - target_user.follower_count: {target_user.follower_count}")
            print(f"Before deletion - user.following_count: {user.following_count}")

            target_user.follower_count -= 1
            target_user.save()

            user.following_count -= 1
            user.save()

            existing_follower.delete()

            print(f"After deletion - target_user.follower_count: {target_user.follower_count}")
            print(f"After deletion - user.following_count: {user.following_count}")

        else:
            target_user.follower_count += 1
            target_user.save()

            user.following_count += 1
            user.save()

            new_follower = Followers.objects.create(is_following=user, user_id=target_user)
            new_follower.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)




def comment(request, id, comment_content):

    if 'user_email' not in request.session:
        return login(request)
    
    # update comment count
    target_post = Posts.objects.get(id=id)
    target_post.comment_count += 1
    target_post.save()

    # insert user who comments
    email = request.session.get('user_email')
    user = CustomUser.objects.get(email=email)

    new_comment = Comments(
        content=comment_content,
        like_count=0,
        comments_by=user,
        posts_id=target_post
    )

    new_comment.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def comment_like(request, id):
    pass


def favorite(request, category_favorite_id, post_id):

    if 'user_email' not in request.session:
        return login(request)
    
    user_email = request.session.get('user_email')
    user = CustomUser.objects.get(email=user_email)
    category_favorite = CategoryFavorites.objects.get(id=category_favorite_id)
    post = Posts.objects.get(id=post_id)
    favorite_check = Favorites.objects.filter(category_favorite_id=category_favorite, posts_id=post).first()

    if favorite_check is not None:
        # delete from favorite
        favorite_check.delete()

        # decrease 1 count
        category_favorite.category_count -= 1
        category_favorite.save()
    else:
        # insert to favorite
        new_favorite = Favorites(category_favorite_id=category_favorite, posts_id=post, user_id=user)
        new_favorite.save()

        # increase 1 count
        category_favorite.category_count += 1
        category_favorite.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
def seen_story(request):

    if 'user_email' not in request.session:
        return login(request)
    
    if request.method == 'POST':
        story_id = request.POST.get('story_id')
        story = Story.objects.get(id=story_id)
        user_email = request.session.get('user_email')
        user = CustomUser.objects.get(email=user_email)

        # Create a Seen_Story object
        seen = Seen_Story.objects.create(story_id=story, seen_by=user)

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Story seen successfully.'})

    # Handle other HTTP methods or invalid requests
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


