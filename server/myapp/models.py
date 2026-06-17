"""数据模型 —— 人才招聘 / 岗位发布系统

说明：薪资、岗位等业务对象沿用前端命名（thing = 岗位/职位）。
"""
from django.db import models


class Admin(models.Model):
    """后台管理员"""
    username = models.CharField(max_length=64, unique=True, verbose_name='账号')
    password = models.CharField(max_length=128, verbose_name='密码（hash）')
    admin_token = models.CharField(max_length=64, null=True, blank=True, verbose_name='登录令牌')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'b_admin'
        verbose_name = '管理员'


class User(models.Model):
    """前台用户（求职者 / HR）"""
    ROLE_CHOICES = (('user', '求职者'), ('hr', '招聘方'))
    STATUS_CHOICES = (('0', '正常'), ('1', '封禁'))

    username = models.CharField(max_length=64, unique=True, verbose_name='账号/工号/邮箱')
    password = models.CharField(max_length=128, verbose_name='密码（hash）')
    nickname = models.CharField(max_length=64, null=True, blank=True, verbose_name='昵称')
    avatar = models.CharField(max_length=255, null=True, blank=True, verbose_name='头像')
    mobile = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机')
    email = models.CharField(max_length=64, null=True, blank=True, verbose_name='邮箱')
    gender = models.CharField(max_length=8, null=True, blank=True, verbose_name='性别')
    description = models.TextField(null=True, blank=True, verbose_name='简介')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='user', verbose_name='角色')
    score = models.IntegerField(default=0, verbose_name='积分')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='0', verbose_name='状态')
    token = models.CharField(max_length=64, null=True, blank=True, verbose_name='登录令牌')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        db_table = 'b_user'
        verbose_name = '用户'


class Classification(models.Model):
    """岗位分类"""
    title = models.CharField(max_length=64, verbose_name='分类名')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_classification'
        verbose_name = '分类'


class Tag(models.Model):
    """标签"""
    title = models.CharField(max_length=64, verbose_name='标签名')

    class Meta:
        db_table = 'b_tag'
        verbose_name = '标签'


class Company(models.Model):
    """公司"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属用户')
    name = models.CharField(max_length=128, verbose_name='公司名')
    logo = models.CharField(max_length=255, null=True, blank=True, verbose_name='logo')
    scale = models.CharField(max_length=32, null=True, blank=True, verbose_name='规模')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='地址')
    description = models.TextField(null=True, blank=True, verbose_name='简介')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_company'
        verbose_name = '公司'


class Thing(models.Model):
    """岗位 / 职位"""
    STATUS_CHOICES = (('1', '上架'), ('2', '下架'))

    title = models.CharField(max_length=128, verbose_name='岗位名')
    cover = models.CharField(max_length=255, null=True, blank=True, verbose_name='封面')
    description = models.TextField(null=True, blank=True, verbose_name='岗位描述')
    salary = models.CharField(max_length=32, null=True, blank=True, verbose_name='薪资')
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='1', verbose_name='状态')
    browse_count = models.IntegerField(default=0, verbose_name='浏览量')
    wish_count = models.IntegerField(default=0, verbose_name='想去人数')
    collect_count = models.IntegerField(default=0, verbose_name='收藏量')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    wish_users = models.ManyToManyField(User, blank=True, related_name='wish_things')
    collect_users = models.ManyToManyField(User, blank=True, related_name='collect_things')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_thing'
        ordering = ['-create_time']
        verbose_name = '岗位'


class Resume(models.Model):
    """简历"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    name = models.CharField(max_length=64, verbose_name='姓名')
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=64, null=True, blank=True)
    education = models.CharField(max_length=32, null=True, blank=True, verbose_name='学历')
    experience = models.CharField(max_length=32, null=True, blank=True, verbose_name='工作年限')
    content = models.TextField(null=True, blank=True, verbose_name='简历内容')
    file = models.CharField(max_length=255, null=True, blank=True, verbose_name='附件')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_resume'
        verbose_name = '简历'


class Order(models.Model):
    """投递记录 / 订单"""
    number = models.CharField(max_length=64, verbose_name='编号')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thing = models.ForeignKey(Thing, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, default='1', verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_order'
        verbose_name = '投递'


class Comment(models.Model):
    """评论"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')
    like_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_comment'
        ordering = ['-create_time']
        verbose_name = '评论'


class Notice(models.Model):
    """公告"""
    title = models.CharField(max_length=128, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_notice'
        ordering = ['-create_time']
        verbose_name = '公告'


class Banner(models.Model):
    """轮播 / 广告位"""
    name = models.CharField(max_length=128, verbose_name='名称')
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name='图片')
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name='跳转链接')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_banner'
        verbose_name = '广告'


class Address(models.Model):
    """收货 / 联系地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, verbose_name='联系人')
    mobile = models.CharField(max_length=20)
    desc = models.CharField(max_length=255, verbose_name='详细地址')
    is_default = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'b_address'
        verbose_name = '地址'


class OpLog(models.Model):
    """操作日志（由 LogMiddleware 写入）"""
    re_ip = models.CharField(max_length=64, null=True, blank=True, verbose_name='IP')
    re_time = models.DateTimeField(auto_now_add=True, verbose_name='请求时间')
    re_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='请求地址')
    re_method = models.CharField(max_length=16, null=True, blank=True, verbose_name='方法')
    re_content = models.CharField(max_length=255, null=True, blank=True, verbose_name='说明')
    access_time = models.CharField(max_length=32, null=True, blank=True, verbose_name='耗时(ms)')

    class Meta:
        db_table = 'b_op_log'
        ordering = ['-re_time']
        verbose_name = '操作日志'
