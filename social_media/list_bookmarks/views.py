from django.shortcuts import render
from general_process.models import CategoryFavorites, Favorites
from django.http import HttpResponseNotFound
from authentication.views import login

# Create your views here.

def list(request, id):

    if 'user_email' not in request.session:
        return login(request)
        
    try:
        id = int(id)  
    except ValueError:
        return HttpResponseNotFound("Invalid user profile")
    
    category = CategoryFavorites.objects.get(id=id)
    favorites = Favorites.objects.filter(category_favorite_id=id)
    
    context = {
        "category_name": category.name,
        "favorites": favorites
    }
    
    return render(request, "list_bookmarks/list_bookmarks.html", context)
