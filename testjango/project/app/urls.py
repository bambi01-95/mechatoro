from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeView, name='home'),

    path('stream/', views.IndexView.as_view(),name="stream"),
    path('video_feed/', views.video_feed_view(), name="video_feed"),

    path('vr/', views.VRView.as_view(),name="vr"),
    path('video_feed_vr/', views.video_feed_vr(), name="video_feed_vr"),  
]
urlpatterns += staticfiles_urlpatterns()