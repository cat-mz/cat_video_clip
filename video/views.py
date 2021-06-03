# -*- coding: utf-8 -*-
from django.http import JsonResponse, FileResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection
from utils.response_code import RETCODE
from utils.send_success import send_message
from celery_tasks.tasks import Video_toClip
from .models import User

import json
import logging

logger = logging.getLogger('video')


from django.http import FileResponse


# 测试版本
def download(request):
    path = './video_clip/out123456.mp4'
    f = open(r'%s' % path, 'rb')
    return FileResponse(f)


class VideoDownLoabView(LoginRequiredMixin, View):
    def get(self, request):
        '''todo：查询功能'''
        # 1.获取异步任务
        user = request.user  # 直接使用,因为LoginRequiredMixin已经校验
        mobile = user.mobile
        try:
            redis_con = get_redis_connection()
            # django-redis返回的byte类型需要改变
            video_path = redis_con.get('video:%s', mobile).decode()
            # 查询出来，并删除之前的信息
            redis_con.delete('video:%s', mobile)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'errno': RETCODE.DATABASESERR, 'errmsg': '服务器繁忙,请稍后重试!'})
        #   1.1 查询进度条
        if video_path is None:
            return JsonResponse({'errno': RETCODE.SOLVENOTERR, 'errmsg': '正在加速处理中'})
        # 1.2 如果处理完成发送结果,并下载剪辑后视频的 URL
        else:
            # 发主动推送剪辑完成事件给⽤户
            send_message(mobile)
            # 方法一：用vsftp结合django可以实现视频上传下载功能
            # 方法二：使用自带功能下载
            f = open(r'%s' % video_path, 'rb')
            return FileResponse(f)

'''
⽤户提交⼀个视频的 URL 格式 https://www.xxxxx.com/xxxx/video_name.mp4
剪辑的起始、终⽌时间戳
url:地址, starttime: 剪辑的起始, endtime:终⽌时间戳,
'''

class VideoDealView(LoginRequiredMixin, View):

    def post(self, request):
        '''todo:提交功能'''
        # 0.判断是否为用户登录
        user = request.user  # 直接使用,因为LoginRequiredMixin已经校验
        user = User.objects.get(username=user.mobile)
        if user:
            return JsonResponse({'errno': RETCODE.USERERR, 'errmsg': '用户错误'})

        # 1.获取json
        data = request.body
        data = json.loads(data)

        # 2.参数检验
        url = data['url']
        startTime = data['starttime']
        endtime = data['endtime']
        if not all([url, startTime, endtime]):
            return JsonResponse({'errno': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必须的参数'})

        # 判断时长大小,用户故意行为
        if startTime > endtime:
            startTime, endtime = endtime, startTime

        # 3.持久化处理,不管是否视频处理,已经提交
        try:
            user.commit += 1
            user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'errno': RETCODE.DATABASESERR, 'errmsg': '服务器繁忙,请稍后重试!'})

        # 4.异步调用 ffmpeg
        try:
            Video_toClip(url, startTime, endtime, user.mobile)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'errno': RETCODE.DATABASESERR, 'errmsg': '服务器繁忙,请稍后重试!'})

        # 5.返回提交成功json格式
        # url 为查询视图的路由,不能放在post提交表单这边否则发生堵塞行为,用户体验拉跨
        return JsonResponse({'errno': RETCODE.OK, 'errmsg': 'OK', 'url': 'video/clip/'})
