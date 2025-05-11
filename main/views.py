from django.shortcuts import render

def index(request):
    return render(request, 'main/mainpage.html')

def mainpage(request):
    return render(request, 'main/mainpagelog.html')