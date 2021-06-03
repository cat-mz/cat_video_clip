from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    commit = models.IntegerField(default=0, verbose_name="用户提交次数")
    mobile = models.CharField(max_length=11, verbose_name="手机号码", unique=True)
    timelength = models.CharField(max_length=100, verbose_name="处理剪辑时长")

    # 修改认证的字段,第三方认证有专门认证视图处理
    USERNAME_FIELD = 'mobile'

    # 创建超级管理员时需要必须设置的字段
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理类'
        verbose_name_plural = verbose_name


'''
1. 接⼝可以正常调⽤，完成既定业务需求。
2. 接⼝通过数据库持久化⽤户提交记录。
3. 接⼝能够鉴别⽤户⾝份。
4. 接⼝⽀持查询剪辑任务的进度。
5. 接⼝⽀持主动推送剪辑完成事件给⽤户。
6. 接⼝拥有完善的错误处理机制。
7. 接⼝拥有良好的⽂档。
8. 考虑到接⼝的部署。
9. 开发过程有代码管理，Commit 记录清晰明确。
10. 有单元测试。
'''
