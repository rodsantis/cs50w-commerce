from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Comment, Bid, Watchlist

CATEGORY_CHOICES = (
    ('Accessories', 'Accessories'),
    ('Books', 'Books'),
    ('Clothing', 'Clothing'),
    ('Cosmetics', 'Cosmetics'),
    ('Eletronics', 'Eletronics'),
    ('Movies', 'Movies'),
    ('Music', 'Music'),
    ('Shoes', 'Shoes'),
    ('Other', 'Other')
)


# New Listing Form
class NewListing(forms.Form):
    title = forms.CharField(label='Title')
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={"style": "height:300px"}))
    price = forms.DecimalField(min_value=1.00, max_digits=10, decimal_places=2)
    img = forms.ImageField(required=False)
    choice = forms.ChoiceField(choices = CATEGORY_CHOICES)


# Bid Form
class BidForm(forms.Form):
    bid = forms.DecimalField(min_value=1.00, max_digits=10, decimal_places=2)

# Comment Form
class CommentForm(forms.Form):
    comment = forms.CharField(max_length=1000, label="Comment", widget=forms.Textarea(attrs={"style": "height:100px"}))


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(active=True)
    })


def index_sold(request):
    return render(request, "auctions/indexsold.html", {
        "listings": Listing.objects.all().filter(active=False)
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
        form = NewListing(request.POST, request.FILES)
        if form.is_valid():
            form_title = form.cleaned_data["title"]
            form_description = form.cleaned_data["description"]
            form_initial_bid = form.cleaned_data["price"]
            form_category = form.cleaned_data["choice"]
            form_img = form.cleaned_data["img"]
            current_user = request.user
            new = Listing(title=form_title, description=form_description, price=form_initial_bid,category=form_category, img=form_img, username=current_user)
            new.save()
        else:
            return render(request, "auctions/createlisting.html", {
                "form": form
            })

    return render(request, "auctions/createlisting.html", {
        "form": NewListing()
    })

def listing_page(request, id):
    # Checking for comment
    comments = Comment.objects.all().filter(listing=id)

    # Checking for the highest bidder if that exists
    listing = Listing.objects.get(pk=id)
    bidder = Bid.objects.all().filter(listing=listing.pk).first()
    if bidder == None:
        pass
    else:    
        bidder = bidder.username

    # Checking and displying page for an Anonymous user
    if request.user.is_anonymous:
        listing_active = Listing.objects.get(pk=id)
        not_active = False
        if listing_active.active == False:
            not_active = True
        return render(request, "auctions/listingpage.html", {
        "listing": Listing.objects.get(pk=id),
        "bid_form": BidForm(),
        "not_active": not_active,
        "winning_bid": bidder,
        "listing_comment": comments
    })
    # IF POST
    if request.method == "POST":
        # Check for the Sell button
        if request.POST.get("sold", False):
            listing_id = request.POST['sold']
            listing = Listing.objects.get(pk=listing_id)
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.pk,)))
        else:
            form = BidForm(request.POST)
            if form.is_valid():
                form_bid = form.cleaned_data["bid"]
                listing = Listing.objects.get(pk=id)
                current_user = request.user
                if float(form_bid) == float(listing.price):
                    bid_exist = Bid.objects.all().filter(listing=listing.pk).first()
                    if bid_exist:
                        return render(request, "auctions/listingpage.html", {
                        "listing": listing,
                        "bid_form": BidForm(),
                        "winning_bid": bidder,
                        "message": "Your bid was too low!",
                        "comment_form": CommentForm(),
                        "listing_comment": comments
                    })
                    else:
                        bid = Bid(listing=Listing.objects.get(pk=id), username=request.user)
                        bid.save()
                        return HttpResponseRedirect(reverse("listing_page", args=(listing.pk,)))
                elif float(form_bid) < float(listing.price):
                    return render(request, "auctions/listingpage.html", {
                        "listing": listing,
                        "bid_form": BidForm(),
                        "winning_bid": bidder,
                        "message": "Your bid was too low!",
                        "comment_form": CommentForm(),
                        "listing_comment": comments
                    })
                else:
                    check_bid = Bid.objects.all().filter(listing=listing.pk).first()
                    if check_bid:
                        if check_bid.username == current_user:
                            listing.price = form_bid
                            listing.save()                     
                        else:
                            check_bid.username = current_user
                            check_bid.save()
                            listing.price = form_bid
                            listing.save()
                            return HttpResponseRedirect(reverse("listing_page", args=(listing.pk,)))
                    else:
                        bid = Bid(listing=Listing.objects.get(pk=id), username=request.user)
                        bid.save()
                        listing.price = float(form_bid)
                        listing.save()
                        return HttpResponseRedirect(reverse("listing_page", args=(listing.pk,)))
    listing_active = Listing.objects.get(pk=id)
    not_active = False
    if listing_active.active == False:
        not_active = True
    return render(request, "auctions/listingpage.html", {
        "listing": Listing.objects.get(pk=id),
        "winning_bid": bidder,
        "bid_form": BidForm(),
        "not_active": not_active,
        "comment_form": CommentForm(),
        "listing_comment": comments
    })


def watchlist(request):
    if request.method == "POST":
        if request.POST.get('watchlist', False):
            listing_id = request.POST['watchlist']
            listing = Listing.objects.get(pk=listing_id)
            current_user = request.user
            exist = Watchlist.objects.all().filter(listing=listing, username=current_user)
            if exist:
                return render(request, "auctions/watchlist.html", {
                    "watch": Watchlist.objects.all().filter(username=request.user),
                    "message": "You are already watching this Listing"
                })
            watch = Watchlist(listing=listing, username=current_user)
            watch.save()
        else:
            listing_id = request.POST['unwatchlist']
            listing = Listing.objects.get(pk=listing_id)
            current_user = request.user
            watch = Watchlist.objects.all().filter(listing=listing, username=current_user)
            watch.delete()

    return render(request, "auctions/watchlist.html", {
        "watch": Watchlist.objects.all().filter(username=request.user)
    })

    
def listing_comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form_comment = form.cleaned_data["comment"]
            print(f"{form_comment}")
            listing = Listing.objects.get(pk=id)
            print(f"Listing: {listing}")
            current_user = request.user
            print(f"User: {current_user}")
            new_comment = Comment(listing=listing, username=current_user, comments=form_comment)
            new_comment.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.pk,)))