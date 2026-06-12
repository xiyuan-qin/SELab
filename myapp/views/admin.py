"""后台管理接口：/myapp/admin/*"""
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from myapp.models import (Admin, Banner, Classification, Comment, Company,
                          Notice, Order, Resume, Thing, User)
from myapp.utils import error, make_token, success, user_to_dict


def _ensure_default_admin():
    """首次运行时种一个默认管理员 admin / 123"""
    if not Admin.objects.exists():
        Admin.objects.create(username='admin', password=make_password('123'))


@csrf_exempt
def admin_login(request):
    """POST 管理员登录，返回 {id, username, admin_token}"""
    _ensure_default_admin()
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    admin = Admin.objects.filter(username=username).first()
    if not admin or not check_password(password, admin.password):
        return error('账号或密码错误')

    admin.admin_token = make_token()
    admin.save(update_fields=['admin_token'])
    return success({
        'id': admin.id,
        'username': admin.username,
        'admin_token': admin.admin_token,
    }, '登录成功')


# ---------------- 用户管理 ----------------

def user_list(request):
    """GET ?username=&page=&limit="""
    qs = User.objects.all().order_by('-id')
    keyword = request.GET.get('username') or request.GET.get('keyword')
    if keyword:
        qs = qs.filter(username__icontains=keyword)

    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    paginator = Paginator(qs, limit)
    rows = paginator.get_page(page)
    return success({
        'list': [user_to_dict(u) for u in rows],
        'total': paginator.count,
    })


@csrf_exempt
def user_create(request):
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '123456')
    if not username:
        return error('账号不能为空')
    if User.objects.filter(username=username).exists():
        return error('账号已存在')
    user = User.objects.create(
        username=username,
        password=make_password(password),
        nickname=request.POST.get('nickname') or username,
        mobile=request.POST.get('mobile'),
        email=request.POST.get('email'),
        token=make_token(),
    )
    return success(user_to_dict(user), '已创建')


@csrf_exempt
def user_update(request):
    uid = request.GET.get('id') or request.POST.get('id')
    user = User.objects.filter(id=uid).first()
    if not user:
        return error('用户不存在')
    for field in ('nickname', 'mobile', 'email', 'gender', 'description', 'status', 'role'):
        if field in request.POST:
            setattr(user, field, request.POST.get(field))
    user.save()
    return success(user_to_dict(user), '已更新')


@csrf_exempt
def user_delete(request):
    uid = request.GET.get('id') or request.POST.get('id')
    User.objects.filter(id=uid).delete()
    return success(msg='已删除')


# ---------------- 概览 ----------------

def overview_count(request):
    return success({
        'user_count': User.objects.count(),
        'thing_count': Thing.objects.count(),
        'company_count': Company.objects.count(),
        'resume_count': Resume.objects.count(),
        'order_count': Order.objects.count(),
        'comment_count': Comment.objects.count(),
        'notice_count': Notice.objects.count(),
        'banner_count': Banner.objects.count(),
        'classification_count': Classification.objects.count(),
    })


def overview_sys_info(request):
    import platform
    import django
    return success({
        'python_version': platform.python_version(),
        'django_version': django.get_version(),
        'system': platform.platform(),
    })
