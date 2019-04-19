from django.db import models

# Create your models here.
# 创建“发布会”表
class Event(models.Model):

    # 发布会标题（字符型，最长100个字符）
    name =  models.CharField(max_length=100)

    # 参加人数（数值型，不限制）
    limit = models.IntegerField()

    # 状态（布尔型，true or false）
    status = models.BooleanField()

    # 地址（字符型，最长200个字符）
    address = models.CharField(max_length=200)

    # 发布会时间（日期类型）
    start_time = models.DateTimeField('events time')

    # 创建时间（日期类型，自动获取当前时间）
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 创建“嘉宾”表
class Guest(models.Model):
    # 关联发布会id
    event = models.ForeignKey(Event)

    # 姓名
    realname = models.CharField(max_length=64)

    # 手机号
    phone = models.CharField(max_length=16)

    # 邮箱
    email = models.EmailField()

    # 签到状态
    sign = models.BooleanField()

    # 创建时间
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "phone")

    def __str__(self):
        return self.realname