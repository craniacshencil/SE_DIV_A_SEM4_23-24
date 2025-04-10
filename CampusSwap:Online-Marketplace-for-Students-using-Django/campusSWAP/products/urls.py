from . import views
from django.urls import path
urlpatterns = [
    path("image_url_gen", views.generate_image_url, name = "image_url_gen"),
    path("upload_listing", views.upload_listing, name = "Upload Listing"),
    path("update_listing", views.update_listing, name = "Update Listing"),
    path("get_resource/<int:resourceId>", views.get_resource, name = "Get Resource"),
    path("user_listings_and_resources/<int:moodleID>", views.user_listings_and_resources, name = "user_listings_and_resources"),
    path("all_approved_listings", views.all_approved_listings, name = "all_approved_listings"),
    path("all_approved_resources", views.all_approved_resources, name = "all_approved_resources"),
    path("upload_resource", views.upload_resource, name = "upload_resource"),
    path("update_resource", views.update_resource, name = "Update resource"),
    path("add_star", views.add_star, name = "Add Star"),
    path("user_starred_resources/<int:moodleID>", views.user_starred_resources, name = "User starred resources"),
    path('simple_search', views.simple_search, name='simple_search'),
    
] 