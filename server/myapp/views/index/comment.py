# Create your views here.
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Comment
from myapp.serializers import CommentSerializer


def _order_field(order_key: str) -> str:
    return '-comment_time' if order_key == 'recent' else '-like_count'


@api_view(['GET'])
def list_api(request):
    thing_id = request.GET.get('thingId')
    order = request.GET.get('order', 'recent')
    if not thing_id:
        return APIResponse(code=1, msg='thingId不能为空')

    comments = Comment.objects.select_related('thing').filter(thing=thing_id).order_by(_order_field(order))
    return APIResponse(code=0, msg='查询成功', data=CommentSerializer(comments, many=True).data)


@api_view(['GET'])
def list_my_comment(request):
    user_id = request.GET.get('userId')
    order = request.GET.get('order', 'recent')
    if not user_id:
        return APIResponse(code=1, msg='userId不能为空')

    comments = Comment.objects.select_related('thing').filter(user=user_id).order_by(_order_field(order))
    return APIResponse(code=0, msg='查询成功', data=CommentSerializer(comments, many=True).data)


@api_view(['POST'])
def create(request):
    ser = CommentSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return APIResponse(code=0, msg='创建成功', data=ser.data)

    print(ser.errors)
    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
def delete(request):
    ids = request.GET.get('ids')
    if not ids:
        return APIResponse(code=1, msg='ids不能为空')

    ids_arr = [s.strip() for s in ids.split(',') if s.strip()]
    Comment.objects.filter(id__in=ids_arr).delete()
    return APIResponse(code=0, msg='删除成功')


@api_view(['POST'])
def like(request):
    comment_id = request.GET.get('commentId')
    comment = Comment.objects.filter(pk=comment_id).first()
    if not comment:
        return APIResponse(code=1, msg='对象不存在')

    comment.like_count = (comment.like_count or 0) + 1
    comment.save()
    return APIResponse(code=0, msg='推荐成功')
