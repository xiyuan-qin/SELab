"""分类 / 公告 / 广告等通用接口"""
from django.views.decorators.csrf import csrf_exempt

from myapp.models import Banner, Classification, Notice
from myapp.utils import error, success


# ---------------- 分类 ----------------

def classification_list(request):
    rows = Classification.objects.all().order_by('id')
    return success([
        {'id': c.id, 'title': c.title} for c in rows
    ])


@csrf_exempt
def classification_create(request):
    title = request.POST.get('title', '').strip()
    if not title:
        return error('分类名不能为空')
    c = Classification.objects.create(title=title)
    return success({'id': c.id, 'title': c.title}, '已创建')


@csrf_exempt
def classification_update(request):
    c = Classification.objects.filter(id=request.GET.get('id') or request.POST.get('id')).first()
    if not c:
        return error('分类不存在')
    c.title = request.POST.get('title', c.title)
    c.save()
    return success({'id': c.id, 'title': c.title}, '已更新')


@csrf_exempt
def classification_delete(request):
    Classification.objects.filter(id=request.GET.get('id') or request.POST.get('id')).delete()
    return success(msg='已删除')


# ---------------- 公告 ----------------

def _notice_dict(n):
    return {
        'id': n.id,
        'title': n.title,
        'content': n.content,
        'create_time': n.create_time.strftime('%Y-%m-%d %H:%M:%S') if n.create_time else None,
    }


def notice_list(request):
    rows = Notice.objects.all()
    return success([_notice_dict(n) for n in rows])


@csrf_exempt
def notice_create(request):
    title = request.POST.get('title', '').strip()
    if not title:
        return error('标题不能为空')
    n = Notice.objects.create(title=title, content=request.POST.get('content', ''))
    return success(_notice_dict(n), '已发布')


@csrf_exempt
def notice_update(request):
    n = Notice.objects.filter(id=request.GET.get('id') or request.POST.get('id')).first()
    if not n:
        return error('公告不存在')
    n.title = request.POST.get('title', n.title)
    n.content = request.POST.get('content', n.content)
    n.save()
    return success(_notice_dict(n), '已更新')


@csrf_exempt
def notice_delete(request):
    Notice.objects.filter(id=request.GET.get('id') or request.POST.get('id')).delete()
    return success(msg='已删除')


# ---------------- 广告 / 轮播 ----------------

def banner_list(request):
    rows = Banner.objects.all().order_by('id')
    return success([
        {'id': b.id, 'name': b.name, 'image': b.image, 'link': b.link} for b in rows
    ])
