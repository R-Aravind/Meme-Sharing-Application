from django.contrib import admin
from django.urls import path, re_path

from memes.views import MemeView

urlpatterns = [
    path('memes/<str:meme_id>', MemeView.as_view()),
    re_path(r'^memes/?$', MemeView.as_view()),
    re_path(r'^comment/?$', MemeView.post_comment),
    re_path(r'^like/?$', MemeView.like_meme)
]
