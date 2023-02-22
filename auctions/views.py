from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv

from auctions.form import AuctionForm
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json


from .models import User, Auction, Bid, Comment

config = cloudinary.config(secure=True)

def index(request):
    auctions_list = Auction.objects.all()
    return render(request, "auctions/index.html", {
        'auctions': auctions_list,
    })

def add(request):
    form = AuctionForm()
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
        
    return render(request, "auctions/add.html", {
        'form': form
    })    


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        
        try:
            user = User.objects.create_user(username, email, password)
 
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



# @login_required
# def add_comment(request, auction_id):
#     auction = get_object_or_404(Auction, pk=auction_id)
#     if request.method == 'POST':
#         text = request.POST.get('text')
#         if text:
#             comment = Comment.objects.create(auction=auction, author=request.user, text=text)
#             comment.save()
#     return redirect('auction_detail', auction_id=auction.id)
