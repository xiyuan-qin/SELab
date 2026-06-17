# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view

from myapp import utils
from myapp.handler import APIResponse
from myapp.models import Classification, Thing, Tag, User
from myapp.serializers import (
    ThingSerializer, ClassificationSerializer, ListThingSerializer,
    DetailThingSerializer, UpdateThingSerializer
)
from myapp.utils import dict_fetchall


def _get_param(request, name, default=None):
    return request.GET.get(name, default)


@api_view(['GET'])
def list_user_thing_api(request):
    user_id = _get_param(request, 'userId')
    if user_id:
        qs = Thing.objects.filter(user=user_id).order_by('-create_time')
        return APIResponse(code=0, msg='查询成功', data=ThingSerializer(qs, many=True).data)


@api_view(['POST'])
def create(request):
    ser = ThingSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return APIResponse(code=0, msg='创建成功', data=ser.data)

    utils.log_error(request, '参数错误')
    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
def update(request):
    pk = _get_param(request, 'id', -1)
    thing = Thing.objects.filter(pk=pk).first()
    if not thing:
        return APIResponse(code=1, msg='对象不存在')

    ser = UpdateThingSerializer(thing, data=request.data)
    if ser.is_valid():
        ser.save()
        return APIResponse(code=0, msg='查询成功', data=ser.data)

    utils.log_error(request, '参数错误')
    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
def delete(request):
    ids = _get_param(request, 'ids', '')
    if ids:
        ids_arr = [s.strip() for s in ids.split(',') if s.strip()]
        Thing.objects.filter(id__in=ids_arr).delete()
        return APIResponse(code=0, msg='删除成功')

    return APIResponse(code=1, msg='对象不存在')


@api_view(['GET'])
def list_api(request):
    keyword = _get_param(request, 'keyword')
    c = _get_param(request, 'c')
    tag = _get_param(request, 'tag')
    sort = _get_param(request, 'sort', 'recent')

    order = '-create_time' if sort == 'recent' else '-pv' if sort in ('hot', 'recommend') else '-create_time'

    if keyword:
        qs = Thing.objects.filter(title__contains=keyword, status='0').order_by(order)

    elif c and int(c) > -1:
        qs = Thing.objects.filter(classification_id__in=[c], status='0').order_by(order)

    elif tag:
        tag_obj = Tag.objects.filter(id=tag).first()
        qs = tag_obj.thing_set.filter(status='0').order_by(order) if tag_obj else Thing.objects.none()

    else:
        qs = Thing.objects.filter(status='0').defer('wish').order_by(order)

    return APIResponse(code=0, msg='查询成功', data=ListThingSerializer(qs, many=True).data)


@api_view(['GET'])
def detail(request):
    pk = _get_param(request, 'id', -1)
    thing = Thing.objects.filter(pk=pk).first()
    if not thing:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    thing.pv = (thing.pv or 0) + 1
    thing.save()
    return APIResponse(code=0, msg='查询成功', data=ThingSerializer(thing).data)


@api_view(['POST'])
def increaseWishCount(request):
    pk = _get_param(request, 'id', -1)
    thing = Thing.objects.filter(pk=pk).first()
    if not thing:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    thing.wish_count = (thing.wish_count or 0) + 1
    thing.save()
    return APIResponse(code=0, msg='操作成功', data=ThingSerializer(thing).data)


@api_view(['POST'])
def increaseRecommendCount(request):
    pk = _get_param(request, 'id', -1)
    thing = Thing.objects.filter(pk=pk).first()
    if not thing:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    thing.recommend_count = (thing.recommend_count or 0) + 1
    thing.save()
    return APIResponse(code=0, msg='操作成功', data=ThingSerializer(thing).data)


@api_view(['POST'])
def addWishUser(request):
    username = _get_param(request, 'username')
    thing_id = _get_param(request, 'thingId')
    try:
        if username and thing_id:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thing_id)
            if user not in thing.wish.all():
                thing.wish.add(user)
                thing.wish_count = (thing.wish_count or 0) + 1
                thing.save()
    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功', data=ThingSerializer(thing).data)


@api_view(['POST'])
def removeWishUser(request):
    username = _get_param(request, 'username')
    thing_id = _get_param(request, 'thingId')
    try:
        if username and thing_id:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thing_id)
            if user in thing.wish.all():
                thing.wish.remove(user)
                thing.wish_count = max((thing.wish_count or 1) - 1, 0)
                thing.save()
    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功')


@api_view(['GET'])
def getWishThingList(request):
    username = _get_param(request, 'username')
    if not username:
        return APIResponse(code=1, msg='username不能为空')
    try:
        user = User.objects.get(username=username)
        things = user.wish_things.all()
        return APIResponse(code=0, msg='操作成功', data=ListThingSerializer(things, many=True).data)
    except Exception as e:
        utils.log_error(request, '操作失败' + str(e))
        return APIResponse(code=1, msg='获取心愿单失败')


@api_view(['POST'])
def addCollectUser(request):
    username = _get_param(request, 'username')
    thing_id = _get_param(request, 'thingId')
    try:
        if username and thing_id:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thing_id)
            if user not in thing.collect.all():
                thing.collect.add(user)
                thing.collect_count = (thing.collect_count or 0) + 1
                thing.save()
    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功', data=DetailThingSerializer(thing).data)


@api_view(['POST'])
def removeCollectUser(request):
    username = _get_param(request, 'username')
    thing_id = _get_param(request, 'thingId')
    try:
        if username and thing_id:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thing_id)
            if user in thing.collect.all():
                thing.collect.remove(user)
                thing.collect_count = max((thing.collect_count or 1) - 1, 0)
                thing.save()
    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功')


@api_view(['GET'])
def getCollectThingList(request):
    username = _get_param(request, 'username')
    if not username:
        return APIResponse(code=1, msg='username不能为空')
    try:
        user = User.objects.get(username=username)
        things = user.collect_things.all()
        return APIResponse(code=0, msg='操作成功', data=ListThingSerializer(things, many=True).data)
    except Exception as e:
        utils.log_error(request, '操作失败' + str(e))
        return APIResponse(code=1, msg='获取收藏失败')


