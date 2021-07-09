from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

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
    context = {
        'new_post_form': NewPostForm(),
        'posts': Post.objects.all().order_by('-time'),
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
        context = {
            'profile': User.objects.get(pk=pk).profile,
        }
        return render(request, 'network/profile.html', context)
