from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import PostForm
from .models import User,Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.db.models import Q


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
    user_id = request.user.id
    context = {
        'posts':posts_paginados,
        'user_id':user_id
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
    return HttpResponseRedirect(reverse("login"))


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



@login_required
def follow(request, follower, followed):
    print(f"{follower} -> {followed}")
    # Supondo que você tenha um modelo UserProfile para os usuários
    follower_obj = User.objects.get(username=follower)
    followed_obj = User.objects.get(username=followed)

    followed_obj.followers.add(follower_obj)
    # Agora você pode acessar os seguidores do seguidor
    if request.method == 'POST':
        return redirect('perfil', user_perfil=followed)


@login_required
def unfollow(request, unfollower, unfollowed):
    print(f"{unfollower} -> {unfollowed}")
    # Supondo que você tenha um modelo UserProfile para os usuários
    unfollower_obj = User.objects.get(username=unfollower)
    unfollowed_obj = User.objects.get(username=unfollowed)

    unfollowed_obj.followers.remove(unfollower_obj)
    # Agora você pode acessar os seguidores do seguidor
    if request.method == 'POST':
        return redirect('perfil', user_perfil=unfollowed)


@login_required
def like(request, id_liker, id_post):
    liker =  User.objects.get(id=id_liker)
    post = Post.objects.get(id = id_post)
    likers = post.liked_by.all()
    if liker in likers:
        post.liked_by.remove(liker)
        print(f"{liker} <- {post} ")
        numberlike = len(post.liked_by.all())
        print(numberlike)
        return JsonResponse({'btnname':'Like','numberlike':numberlike})

    else:
        post.liked_by.add(liker)
        print(f"{liker} -> {post}")
        numberlike = len(post.liked_by.all())
        print(numberlike)
        return JsonResponse({'btnname':'Dislike','numberlike':numberlike})
  
    


