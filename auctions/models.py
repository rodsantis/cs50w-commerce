from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models

#CATEGORY_LIST = ['Clothing', 'Shoes', 'Cosmetics', 'Books', 'Movies', 'Music', 'Accessories', 'Eletronics']


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # date = models.DateTimeField()


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    comments = models.CharField(max_length=1000)


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    bids = models.DecimalField(max_digits=10, decimal_places=2)