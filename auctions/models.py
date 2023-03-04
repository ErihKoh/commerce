from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=1)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, id: {self.id}"

    def get_comments(self):
        return self.comments.order_by('-created_at')
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auctions = models.ManyToManyField(Auction)    


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.user} - {self.auction.name}: {self.amount}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
