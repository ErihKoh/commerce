from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=64)
    url = models.TextField()

    def __str__(self):
        return f"{self.url}"


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    current_bid = models.IntegerField()
    creation_date = models.DateTimeField()
    available = models.BooleanField()
    description = models.CharField(max_length=64)
    photos = models.ManyToManyField(Photo, related_name='photos', blank=True)
    auction_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="author")

    def __str__(self):
        return f"{self.id} {self.name}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    auction_bid = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bider")

    def __str__(self):
        return f"{self.price}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_to = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction")
    text = models.TextField()

    def __str__(self):
        return f"{self.commenter} {self.comment_to} {self.text}"

class WatchList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    auctions = models.ManyToManyField(Auction, related_name="auctions", blank=True)
    
    def __str__(self):
        return f"{self.user}'s watchlist"

 