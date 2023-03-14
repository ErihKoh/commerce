from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Max
from decimal import Decimal
import datetime

# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv

from auctions.form import AuctionForm, EditAuctionForm, CommentForm, BidForm

load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

from .models import User, Auction, Bid, Comment, Watchlist

config = cloudinary.config(secure=True)


def index(request):
    auctions_list = Auction.objects.all()
    auction = Auction.objects.filter(winner=request.user)
    print(auction)
    return render(request, "auctions/index.html", {
        'auctions': auctions_list,
        'winning_lots': auction
    })


def winning_lots(request):
    auction = Auction.objects.filter(winner=request.user)
    return render(request, "auctions/winning-lot.html", {
        'winning_lots': auction
    })

def my_list(request):
    auctions_list = Auction.objects.all()
    
    user = request.user
    return render(request, "auctions/my-list.html", {
        'auctions': auctions_list,
        'user': user,
    })


def watching_list(request):
    watchlist = Watchlist.objects.all()
    user = request.user
    return render(request, "auctions/watch-list.html", {
        'watchlist': watchlist,
        'user': user,
    })


def add_to_watchlist(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.create(user=request.user, auction=auction)
        watchlist.save()

    return redirect('detail', auction_id)


def remove_from_watchlist(request, auction_id):
    watchlist = Watchlist.objects.all()
    global watchlist_item 
    for i in watchlist:
        if i.auction.id == auction_id:
            watchlist_item = i

    watchlist_item.delete()

    print(f'Item has been deleted from watchlist')
    return redirect('detail', auction_id)


def add_comment(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.auction = auction
            comment.author = request.user
            comment.save()
            return redirect('detail', auction_id=auction_id)
    return render(request, "auctions/add_comment.html", {
        'form': form
    })

def bid(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    form = BidForm()
    
    if request.method == 'POST':
        max_bid = Bid.objects.filter(auction=auction).aggregate(Max('amount'))['amount__max']
        form = BidForm(request.POST)
        
        if form.is_valid():
            amount = Decimal(request.POST.get('amount'))
            if not max_bid:
                max_bid = auction.price
            if amount <= max_bid:
              return HttpResponse('Amount have to higher than the current price')
            bid = form.save(commit=False)
            bid.auction = auction
            bid.bidder = request.user
            bid.save()
            
            return redirect('detail', auction_id=auction_id)  
    return render(request, "auctions/bid.html", {
        'form': form,
    })


def add(request):
    form = AuctionForm()
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            upload = request.FILES['image_url']
            img_url = cloudinary.uploader.upload(upload, folder="commerce/")
            auction = form.save(commit=False)
            auction.seller = request.user
            auction.image_url = img_url['url']
            auction.save()
            return redirect("/")

    return render(request, "auctions/add.html", {
        'form': form
    })


def edit(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if request.method == 'POST':
        form = EditAuctionForm(request.POST, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('detail', auction_id=auction_id)
    else:
        form = EditAuctionForm(instance=auction)
    return render(request, 'auctions/edit.html', {'form': form, 'auction_id': auction_id})


def delete(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    auction.delete()

    print(f'{auction.name} has been deleted')

    return redirect("/")


def detail(request, auction_id):
    # Bid.objects.all().delete()
    auction = get_object_or_404(Auction, pk=auction_id)
    current_date = datetime.datetime.now().date()
    comments = Comment.objects.filter(auction=auction)
    max_bid = Bid.objects.filter(auction=auction).aggregate(Max('amount'))['amount__max']
    top_bidder = None
    winner = None
    if max_bid is not None:
        top_bidder = Bid.objects.filter(auction=auction, amount=max_bid).first().bidder
        print(f"Top Bidder: {top_bidder}, Max Bid: {max_bid}")
    else:
        print("There are no bids for the current auction.")
    seller  = auction.seller
    user = request.user
    auctions = []
    watchlist = Watchlist.objects.all()    
    for item in watchlist:
        auctions.append(item.auction.id)

    if top_bidder and (auction.end_date == current_date or auction.is_available == False): 

        winner = top_bidder
        auction.winner = winner
        auction.save()

    context = {'auction': auction, 'user': user, 
               'seller': seller, 
               'auctions_id': auctions, 
               'comments': comments, 'winner': winner or None,
               'current_price': max_bid or 'No bid', 'bidder': top_bidder or 'No bidder'}
    return render(request, "auctions/detail.html", context)


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



