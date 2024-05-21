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
    # TODO add the image entry also

    def __str__(self):
        return f"{self.title}: {self.description}, ${self.price}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    comments = models.CharField(max_length=1000)

    def __str__(self):
        return f"Listing: {self.listing}, Comment: {self.comments}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    bids = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Listing: {self.listing}, Bids: {self.bids}"