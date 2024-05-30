from django.shortcuts import render
from authentication.views import login

# Create your views here.

def index(request):

    if 'user_email' not in request.session:
        return login(request)
        
    return render(request, "chat/chat.html")
