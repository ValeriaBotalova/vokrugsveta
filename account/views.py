from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render

@login_required
def history_view(request):
    context = {
        'user': request.user 
    }
    return render(request, 'account/history.html', context)

def logout_view(request):
    logout(request)
    return render(request,'main/mainpage.html')