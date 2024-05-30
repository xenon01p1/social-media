from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import CustomUser
from authentication.views import login
from explore.models import Posts
from general_process.models import CategoryFavorites
from my_profile.models import Followers, Report
from home.models import Story
import os
from django.utils import timezone
# from django.shortcuts import get_object_or_404
# from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from django.contrib.sessions.models import Session

def profile(request):

    if 'user_email' not in request.session:
        return login(request)
    
    email = request.session.get('user_email')
    user_data = CustomUser.objects.get(email=email)
    user_post = Posts.objects.filter(insert_by_id=user_data.id)
    post_count = user_post.count()
    category_favorites = CategoryFavorites.objects.filter(user_id=user_data.id)
    get_story = Story.objects.filter(insert_by_id=user_data).order_by('-id').first()

    if timezone.now() < get_story.delete_datetime:
        story = get_story
    else:
        story = None

    print(story)

    context = {
        "user": user_data,
        "posts": user_post,
        "post_count": post_count,
        "category_favorites": category_favorites,
        "story": story
    }

    success = request.GET.get('success')
    if success:
        context['success'] = True
        context['toast_message'] = "Success!"
        context['sub_message'] = "Your password has been updated"

    return render(request, "my_profile/profile.html", context)


def other_profile(request, id):

    if 'user_email' not in request.session:
        return login(request)
    
    try:
        id = int(id)  # Convert id to an integer
    except ValueError:
        # Handle the case where id is not a valid integer, for example, by returning a 404 response
        return HttpResponseNotFound("Invalid user profile")
    other_user_data = CustomUser.objects.get(id=id)
    other_user_id = other_user_data.id

    user_email = request.session.get('user_email')
    user_id = CustomUser.objects.get(email=user_email).id

    user_post = Posts.objects.filter(insert_by_id=other_user_id)
    post_count = user_post.count()

    try:
        is_following = Followers.objects.get(is_following=user_id, user_id=other_user_id)
    except ObjectDoesNotExist:
        is_following = None

    context = {
        "user": other_user_data,
        "posts": user_post,
        "post_count": post_count,
        "is_following": is_following
    }

    return render(request, "my_profile/other_profile.html", context)


def edit_profile(request):

    if 'user_email' not in request.session:
        return login(request)

    user_id = request.session.get('id')
    try:
        user_data = CustomUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        user_data = None

    if request.method == 'POST':

        profile_picture = request.FILES.get('profile_picture')
        description = request.POST.get('description')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        city = request.POST.get('city')

        new_filename = None

        if profile_picture:
            filename, extension = os.path.splitext(profile_picture.name)
            new_filename = f"profile_pic_{timezone.now().strftime('%H_%M_%S')}_{filename}{extension}"
            user_data.profile_picture = new_filename

            # Save the file to the media folder
            with open(os.path.join(settings.MEDIA_ROOT, new_filename), 'wb+') as destination:
                for chunk in profile_picture.chunks():
                    destination.write(chunk)

        user_data.description = description
        user_data.birth_date = birth_date
        user_data.gender = gender
        user_data.country = country
        user_data.city = city

        user_data.save()
        return redirect('/my_profile/')
    
    countries = [
        "United States",
        "Canada",
        "United Kingdom",
        "Germany",
        "France",
        "Japan",
        "China",
        "Australia",
        "Brazil",
        "India"
    ]

    cities = [
        "New York", 
        "Los Angeles", 
        "Montreal",
        "Vancouver",
        "Berlin",
        "Paris","Tokyo",
        "Yokohama",
        "Osaka","Shanghai",
        "Beijing",
        "Sydney",
        "Melbourne",
        "Sao Paulo",
        "Mumbai"
    ]
    
    context = {
        "user": user_data,
        "countries": countries,
        "cities": cities
    }

    return render(request, "my_profile/edit_profile.html", context)


def change_password(request):

    if 'user_email' not in request.session:
        return login(request)

    if request.method == "POST":
        user_id = request.session.get('id')
        user = CustomUser.objects.get(id=user_id)

        old_password = request.POST.get('old_password').strip()
        new_password = make_password(request.POST.get('new_password').strip())

        if check_password(old_password, user.password):
            user.password = new_password
            user.save()
            return HttpResponseRedirect(reverse('my_profile:profile') + '?success=true')
            # reverse is used for redirecting with the sam econfiguration as the last one
        
        else:
            context = {
                'success': False,
                'toast_message': 'Sorry, wrong old password',
                'sub_message': 'Your old password is not correct. Please try again.'
            }

            return render(request, "my_profile/change_password.html", context)
        
    context = {
        'success': True,
        'toast_message': 'Sorry, wrong old password',
        'sub_message': 'Your old password is not correct. Please try again.'
    }

    return render(request, "my_profile/change_password.html", context)


def followers_list(request):

    if 'user_email' not in request.session:
        return login(request)
    
    user_email = request.session.get('user_email')
    user_id = CustomUser.objects.get(email=user_email).id
    followers = Followers.objects.filter(user_id=user_id)

    context = {
        'followers': followers
    }

    return render(request, "my_profile/list_follower.html", context)


def followings_list(request):

    if 'user_email' not in request.session:
        return login(request)
    
    user_email = request.session.get('user_email')
    user_id = CustomUser.objects.get(email=user_email).id
    followings = Followers.objects.filter(is_following=user_id)

    context = {
        'followings': followings
    }

    return render(request, "my_profile/list_following.html", context)


def logout_view(request):

    if 'user_email' not in request.session:
        return login(request)
    
    # Store the current URL in the session
    request.session['previous_url'] = request.build_absolute_uri()
    
    # Clear the session and logout the user
    request.session.flush()
    logout(request)
    
    # Redirect to the previously stored URL
    return HttpResponseRedirect(request.session.get('previous_url', '/'))


def report(request, id):

    if 'user_email' not in request.session:
        return login(request)
    
    other_user_id   = id
    other_user      = CustomUser.objects.get(id=other_user_id)
    user_email      = request.session.get('user_email')
    user            = CustomUser.objects.get(email=user_email)

    if request.method == 'POST':
        report_content = request.POST.get('report_content')
        new_report = Report(user_report=other_user, report_content=report_content, insert_by=user)
        new_report.save()

        return render(request, "my_profile/report.html")

    return render(request, "my_profile/report.html")