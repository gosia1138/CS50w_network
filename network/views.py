import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Profile, Post, CommentPost
from .forms import NewPostForm


def index(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            p = Post(
                author=request.user,
                content=form.cleaned_data['content']
            )
            p.save()
            return redirect(reverse('index'))
    else:
        posts = Post.objects.all().order_by('-time')
        page = request.GET.get('page', 1)
        pag = Paginator(posts, 5)
        post_page = pag.page(page)
        context = {
            'new_post_form': NewPostForm(),
            'posts': post_page,
            'page_count': pag.num_pages,
        }
        return render(request, "network/index.html", context)


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
def profile_view(request, pk):
    if request.method == "POST":
        user = User.objects.get(pk=pk)
        if 'follow' in request.POST:
            request.user.profile.followed.add(user)
        elif 'unfollow' in request.POST:
            request.user.profile.followed.remove(user)
        else:
            pass
        return redirect(reverse('profile', kwargs={'pk': pk}))
    else:
        user = User.objects.get(pk=pk)
        posts = user.posts()
        page = request.GET.get('page', 1)
        pag = Paginator(posts, 5)
        post_page = pag.page(page)
        context = {
            'profile': user.profile,
            'posts': post_page,
            'page_count': pag.num_pages,
        }
        return render(request, 'network/profile.html', context)

@login_required
def following_view(request):
    posts = request.user.profile.followed_posts()
    page = request.GET.get('page', 1)
    pag = Paginator(posts, 5)
    post_page = pag.page(page)
    context = {
        'posts': post_page,
        'page_count': pag.num_pages,
    }
    return render(request, "network/following.html", context)


# ----- APIs -----

@csrf_exempt
@login_required
def edit_post(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse(email.serialize())
    elif request.method == 'PUT' and post.author == request.user:
        data = json.loads(request.body)
        if data.get('content') is not None:
            post.content = data['content']
            post.save()
        return HttpResponse(status=200)
    return HttpResponse(status=403)
