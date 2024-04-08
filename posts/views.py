from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import CommentForm,ContactForm
from django.core.mail import send_mail
from .models import Post, User,Comment
from .forms import PostForm

# Create your views here.

def index(request):
    posts = Post.objects.all()

    ctx = {'posts': posts}
    return render(request, 'index.html', ctx)


def post(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.all()
    ctx = {
        'post': post,
        'comments':comments
    }
    return render(request, 'post.html', ctx)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistre les données du formulaire dans le modèle de contact
            subject = "Website Inquiry" 
            body = {
                'first_name': form.cleaned_data['first_name'], 
                'last_name': form.cleaned_data['last_name'], 
                'email': form.cleaned_data['email'], 
                'message': form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("index")
    else:
        form = ContactForm()
    return render(request, "contact.html", {'form': form})


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect('/post/' + str(post.id))  # Redirige vers la page du post nouvellement créé
    else:
        form = PostForm()
    
    ctx = {'form': form}
    return render(request, 'createpost.html', ctx)

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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


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
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

@login_required
def like_dislike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    like, created = LikeDislike.objects.get_or_create(user=user, post=post)

    if request.GET.get('action') == 'like':
        like.like = True
    elif request.GET.get('action') == 'dislike':
        like.like = False

    like.save()

    return redirect('post_detail', post_id=post.id)