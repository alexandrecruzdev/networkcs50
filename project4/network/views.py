from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from .models import User,Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
def index(request):
    form = PostForm()
    posts = Post.objects.all().order_by('-id')
    if request.method == 'POST':
       new_post = Post(content=request.POST['post'], user=request.user)
       new_post.save()
       print('saved')

    paginator = Paginator(posts,10)
    page = request.GET.get('pagina')
    posts_paginados = paginator.get_page(page)
    context = {
        'posts':posts_paginados
    }
    return render(request, "network/index.html",context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def perfil(request,user_perfil):
    user_request = User.objects.get(username = request.user)
    user_perfil = User.objects.get(username = user_perfil)

    len_followers = len(user_perfil.followers.all())
    len_following = len(user_perfil.following.all())

    followers = user_perfil.followers.all()
    is_following = user_request in followers
    
    posts = Post.objects.filter(user = user_perfil).order_by('-id')

    paginator = Paginator(posts,10)
    page = request.GET.get('pagina')
    posts_paginados = paginator.get_page(page)
    user_perfil_request_user = str(request.user) == str(user_perfil)
    context = {
        'posts':posts_paginados,
        'len_followers':len_followers,
        'len_following':len_following,
        'user_perfil_request_user':user_perfil_request_user,
        'is_following':is_following
    }
    return render(request,'network/perfil.html',context)





@login_required
def following(request):
    user = User.objects.get(username = request.user)
    following = user.following.all()
    all_posts = Post.objects.all()
    posts_filtered = []

    for user in following:
        for post in all_posts:
            if user == post.user:
                posts_filtered.append(post)
       

    paginator = Paginator(posts_filtered,10)
    page = request.GET.get('pagina')
    posts_paginados = paginator.get_page(page)
    context = {
        'posts':posts_paginados
    }
    return render(request,'network/following.html',context)

@login_required
def editPost(request,id,new_value):
    post = Post.objects.get(pk=id)
    if request.method == 'POST' and request.user == post.user:    
        post.content = new_value
        post.save()
        print(f"{id} - {new_value}")
    return HttpResponse('teste')