from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('controller/', views.controllerView, name='controller'),
    # for iPhone (basic)
    path('stream/', views.IndexView.as_view(),name="stream"),
    # for web app
    path('web/', views.webView.as_view(),name="web"),
    # 前方カメラの出力
    path('video_feed/', views.video_feed_view_f(), name="video_feed"),
    # 後方カメラの出力
    path('video_feed_back/', views.video_feed_view_b(), name="video_feed_back"),

    # for iPhone (VR)
    path('vr/', views.VRView.as_view(),name="vr"),
    path('video_feed_vr/', views.video_feed_vr(), name="video_feed_vr"),  
]
urlpatterns += staticfiles_urlpatterns()