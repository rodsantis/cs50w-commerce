from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sold", views.index_sold, name="index_sold"),
    path("category", views.index_category, name="index_category"),
    path("category/<str:category>", views.category_search, name="category_search"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing", views.index, name="listing_index"),
    path("listing/<int:id>", views.listing_page, name="listing_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.listing_comment, name="listing_comment")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
