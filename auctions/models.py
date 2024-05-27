from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    img = models.ImageField(upload_to="auctions/uploads/images", blank=True, null=True, default=None)
    # date = models.DateTimeField()
    # TODO add the image entry also

    def __str__(self):
        return f"{self.title}: {self.description}, ${self.price}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    comments = models.CharField(max_length=1000)

    def __str__(self):
        return f"Listing: {self.listing}, Comment: {self.comments}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bids = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Listing: {self.listing}, Bids: {self.bids}"


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchedlisting")
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")

    def __str__(self):
        return f"The listing {self.listing} is being watched by {self.username}"