"""岗位/职位接口：/myapp/index/thing/*"""
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from myapp.models import Classification, Company, Thing, User
from myapp.utils import error, success, thing_to_dict


def _get_user(request):
    uid = request.GET.get('user_id') or request.POST.get('user_id')
    return User.objects.filter(id=uid).first()


def list_thing(request):
    """GET 岗位列表 ?keyword=&classification_id=&page=&limit="""
    qs = Thing.objects.filter(status='1')
    keyword = request.GET.get('keyword') or request.GET.get('title')
    if keyword:
        qs = qs.filter(title__icontains=keyword)
    cid = request.GET.get('classification_id')
    if cid:
        qs = qs.filter(classification_id=cid)

    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    paginator = Paginator(qs, limit)
    rows = paginator.get_page(page)
    return success({
        'list': [thing_to_dict(t) for t in rows],
        'total': paginator.count,
    })


def list_user_thing(request):
    """GET 某用户发布的岗位 ?user_id="""
    user = _get_user(request)
    if not user:
        return error('用户不存在')
    company_ids = Company.objects.filter(user=user).values_list('id', flat=True)
    qs = Thing.objects.filter(company_id__in=list(company_ids))
    return success([thing_to_dict(t) for t in qs])


def detail(request):
    """GET 岗位详情 ?id= （浏览量+1）"""
    thing = Thing.objects.filter(id=request.GET.get('id')).first()
    if not thing:
        return error('岗位不存在')
    thing.browse_count += 1
    thing.save(update_fields=['browse_count'])
    return success(thing_to_dict(thing))


@csrf_exempt
def create(request):
    title = request.POST.get('title', '').strip()
    if not title:
        return error('岗位名不能为空')
    thing = Thing.objects.create(
        title=title,
        cover=request.POST.get('cover'),
        description=request.POST.get('description'),
        salary=request.POST.get('salary'),
        classification_id=request.POST.get('classification_id') or None,
        company_id=request.POST.get('company_id') or None,
        status=request.POST.get('status', '1'),
    )
    return success(thing_to_dict(thing), '已发布')


@csrf_exempt
def update(request):
    thing = Thing.objects.filter(id=request.GET.get('id') or request.POST.get('id')).first()
    if not thing:
        return error('岗位不存在')
    for field in ('title', 'cover', 'description', 'salary', 'status'):
        if field in request.POST:
            setattr(thing, field, request.POST.get(field))
    if request.POST.get('classification_id'):
        thing.classification_id = request.POST.get('classification_id')
    if request.POST.get('company_id'):
        thing.company_id = request.POST.get('company_id')
    thing.save()
    return success(thing_to_dict(thing), '已更新')


@csrf_exempt
def delete(request):
    Thing.objects.filter(id=request.GET.get('id') or request.POST.get('id')).delete()
    return success(msg='已删除')


# ---------------- 收藏 / 想去 ----------------

def _toggle(request, m2m_attr, count_attr, add=True):
    thing = Thing.objects.filter(id=request.GET.get('thing_id') or request.POST.get('thing_id')).first()
    user = _get_user(request)
    if not thing or not user:
        return error('参数错误')
    m2m = getattr(thing, m2m_attr)
    if add:
        m2m.add(user)
    else:
        m2m.remove(user)
    setattr(thing, count_attr, m2m.count())
    thing.save(update_fields=[count_attr])
    return success(msg='操作成功')


@csrf_exempt
def add_wish_user(request):
    return _toggle(request, 'wish_users', 'wish_count', add=True)


@csrf_exempt
def remove_wish_user(request):
    return _toggle(request, 'wish_users', 'wish_count', add=False)


@csrf_exempt
def add_collect_user(request):
    return _toggle(request, 'collect_users', 'collect_count', add=True)


@csrf_exempt
def remove_collect_user(request):
    return _toggle(request, 'collect_users', 'collect_count', add=False)


def get_wish_thing_list(request):
    user = _get_user(request)
    if not user:
        return error('用户不存在')
    return success([thing_to_dict(t) for t in user.wish_things.all()])


def get_collect_thing_list(request):
    user = _get_user(request)
    if not user:
        return error('用户不存在')
    return success([thing_to_dict(t) for t in user.collect_things.all()])
