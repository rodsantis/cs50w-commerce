from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Comment, Bid


# New Listing Form
class NewListing(forms.Form):
    title = forms.CharField(label='Title')
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={"style": "height:300px"}))
    price = forms.DecimalField(min_value=1.00, max_digits=10, decimal_places=2)


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request, *args, **kwargs):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            form_title = form.cleaned_data["title"]
            form_description = form.cleaned_data["description"]
            form_initial_bid = form.cleaned_data["price"]
            current_user = request.user
            new = Listing(title=form_title, description=form_description, price=form_initial_bid, username=current_user)
            new.save()
        else:
            return render(request, "auctions/createlisting.html", {
                "form": form
            })

    return render(request, "auctions/createlisting.html", {
        "form": NewListing()
    })

def listing_page(request, name):
    return render(request, "auctions/listingpage.html", {
        "listing": Listing.objects.get(title=name)
    })