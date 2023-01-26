from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User, Auction, Comment, Bid, Category

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
