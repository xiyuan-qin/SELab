"""前台用户相关接口：/myapp/index/user/*"""
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt

from server1.myapp.models import User
from server1.myapp.utils import error, make_token, success, user_to_dict


@csrf_exempt
def login(request):
    """POST 登录，返回 {id, username, token}"""
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    if not username or not password:
        return error('账号或密码不能为空')

    user = User.objects.filter(username=username).first()
    if not user or not check_password(password, user.password):
        return error('账号或密码错误')
    if user.status == '1':
        return error('账号已被封禁')

    user.token = make_token()
    user.save(update_fields=['token'])

    data = user_to_dict(user)
    data['token'] = user.token
    return success(data, '登录成功')


@csrf_exempt
def register(request):
    """POST 注册"""
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    repassword = request.POST.get('repassword', '')

    if not username or not password:
        return error('账号或密码不能为空')
    if password != repassword:
        return error('两次输入的密码不一致')
    if User.objects.filter(username=username).exists():
        return error('该账号已被注册')

    # 身份：求职者 user / 招聘方 hr，非法值一律按求职者
    role = request.POST.get('role', 'user')
    if role not in ('user', 'hr'):
        role = 'user'

    user = User.objects.create(
        username=username,
        password=make_password(password),
        nickname=username,
        role=role,
        token=make_token(),
    )
    return success({'id': user.id, 'username': user.username, 'role': user.role}, '注册成功')


def info(request):
    """GET 用户详情，?id="""
    uid = request.GET.get('id')
    user = User.objects.filter(id=uid).first()
    if not user:
        return error('用户不存在')
    return success(user_to_dict(user))


@csrf_exempt
def update(request):
    """POST 更新资料，?id= + 表单字段"""
    uid = request.GET.get('id') or request.POST.get('id')
    user = User.objects.filter(id=uid).first()
    if not user:
        return error('用户不存在')

    for field in ('nickname', 'avatar', 'mobile', 'email', 'gender', 'description'):
        if field in request.POST:
            setattr(user, field, request.POST.get(field))
    user.save()
    return success(user_to_dict(user), '已更新')


@csrf_exempt
def update_pwd(request):
    """POST 修改密码，?id= ，body: oldPassword/newPassword"""
    uid = request.GET.get('id') or request.POST.get('id')
    user = User.objects.filter(id=uid).first()
    if not user:
        return error('用户不存在')

    old_pwd = request.POST.get('oldPassword') or request.POST.get('old_password', '')
    new_pwd = request.POST.get('newPassword') or request.POST.get('new_password', '')
    if not new_pwd:
        return error('新密码不能为空')
    if old_pwd and not check_password(old_pwd, user.password):
        return error('原密码错误')

    user.password = make_password(new_pwd)
    user.save(update_fields=['password'])
    return success(msg='密码已修改')
