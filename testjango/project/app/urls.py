from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # path('',views.index, name='index'),
    path('', views.IndexView.as_view()),
    path('video_feed/', views.video_feed_view(), name="video_feed"),
]
urlpatterns += staticfiles_urlpatterns()