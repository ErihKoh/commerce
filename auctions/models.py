from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    category = models.CharField(max_length=64) 
    image_url = models.URLField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    isAvailable = models.BooleanField(default=True)

    

    def __str__(self):
        return f"Auction id: {self.id}, title: {self.title}, seller: {self.author}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.user} bid {self.bid_price} $ on {self.auction}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Comment {self.id} on auction {self.auction} made by {self.user}"

  
