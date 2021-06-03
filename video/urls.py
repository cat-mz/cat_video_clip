from django.urls import path
from .views import VideoDealView, VideoDownLoabView, download

urlpatterns = [
    path('clip/', VideoDealView.as_view(), name='clip'),  # 视频处理视图
    path('', download),  # 视频下载测试版本
    path('download/', VideoDownLoabView.as_view(), name='download')  # 视频下载
]
