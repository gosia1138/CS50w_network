import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Profile, Post
from .forms import NewPostForm, ProfileUpdateForm


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
        pag = Paginator(posts, 10)
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
            messages.success(request, "You are now logged in!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request, "Invalid username and/or password")
            return render(request, "network/login.html")
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
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        if 'profile_pic_update' in request.POST and request.user == user:
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile picture has been updated')
            else:
                messages.error(request, 'Provide a valid picture file')
            return redirect(reverse('profile', kwargs={'pk': pk}))
        else:
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
        pag = Paginator(posts, 10)
        post_page = pag.page(page)
        form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'profile': user.profile,
            'posts': post_page,
            'page_count': pag.num_pages,
            'form': form,
        }
        return render(request, 'network/profile.html', context)




@login_required
def following_view(request):
    posts = request.user.profile.followed_posts()
    page = request.GET.get('page', 1)
    pag = Paginator(posts, 10)
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

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data['route'] == 'edit' and post.author == request.user:
            if data.get('content') is not None:
                post.content = data['content']
                post.save()
                return HttpResponse(status=200)
            else:
                return JsonResponse({"error": "Post not found"}, status=404)
        elif data['route'] == 'like':
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                return JsonResponse({
                    "likes_count": post.likes_count(),
                    }, status=200)
            else:
                post.likes.add(request.user)
                return JsonResponse({
                    "likes_count": post.likes_count(),
                    }, status=200)
    else:
        return HttpResponse(status=403)
