from celery import Celery
from ffmpy import FFmpeg
import wget  # 使用wget下载路由中的视频
import re
import uuid
from django_redis import get_redis_connection

# 创建一个Celery类的实例对象
app = Celery('celery.task', broker='redis://127.0.0.1:6379/8')

'''todo:启动命令celery -A celery_tasks.tasks worker -l info'''


@app.task
def Video_toClip(url, startTime, endTime, mobile):
    '''
    :param url: video URL
    :param startTime:  剪辑开始时间
    :param endTime: 剪辑结束时间
    :return:
    '''
    output_name = re.split('/', url)[-1] + str(uuid.uuid1())  # 输出文件名.视频格式 + uuid避免重复提交名字重复
    wget.download(url=url, out='../video_storage/{}'.format(output_name))

    input_path = './video_storage/' + output_name  # 视频储存路由
    # 创建连接到redis的对象
    redis_con = get_redis_connection()
    # 保存视频储存路由到redis中，并设置有效期
    redis_con.setex('video:%s' % mobile, 24 * 60 * 60, input_path)
    # 如果用户重新提交那么将原有的redis的视频路由重置
    ff = FFmpeg(inputs={
        input_path: "-ss {} -t {} -i {} -vcodec copy -acodec copy ../video_clip/{}".format(startTime, endTime,
                                                                                           input_path,
                                                                                           output_name)
    })
    ff.run()


