"""xmeme_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from memes.views import MemeView
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/memes/<str:meme_id>', MemeView.as_view()),
    path('api/memes/', MemeView.as_view()),
    path('api/comment/', MemeView.post_comment),
    path('api/like/', MemeView.like_meme)
]
