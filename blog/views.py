from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blog import models
from .models import Post
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




def signup(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        email= request.POST.get('uemail')
        password = request.POST.get('upassword')
        newUser = User.objects.create_user(username=name, email=email, password=password)
        newUser.save()
        return redirect('/loginn')
    return render(request, 'blog/signup.html')




def loginn(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('upassword')
        userr = authenticate(request, username=name, password=password)
        if userr is not None:
            login(request, userr)
            return redirect('/home')
        else:
            return redirect('/login')

    return render(request, 'blog/login.html')




def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)



def newPost(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        npost = models.Post(title=title, content=content, author=request.user)
        npost.save()
        return redirect('/home')
    
    return render(request, 'blog/newpost.html')




def myPost(request):
    context = {
        'posts': Post.objects.filter(author= request.user)
    }
    return render(request, 'blog/mypost.html', context)

def signout(request):
    logout(request)
    return redirect('/loginn')


@login_required
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Post deleted successfully!')  # Success message
        return redirect('/home')
        
    else:
        return HttpResponseForbidden("You are not authorized to delete this post.")