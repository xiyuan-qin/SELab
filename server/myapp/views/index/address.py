# Create your views here.
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Address
from myapp.serializers import AddressSerializer


def _q(request, key, default=None):
    return request.GET.get(key, default)


def _is_true(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('1', 'true', 'yes', 'on')


@api_view(['GET'])
def list_api(request):
    user_id = _q(request, 'userId')
    if not user_id:
        return APIResponse(code=1, msg='userId不能为空')

    qs = Address.objects.filter(user=user_id).order_by('-create_time')
    return APIResponse(code=0, msg='查询成功', data=AddressSerializer(qs, many=True).data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):
    data = request.data
    desc = data.get('desc')
    user = data.get('user')
    default = _is_true(data.get('default', False))

    if not desc or not user:
        return APIResponse(code=1, msg='不能为空')

    if default:
        Address.objects.filter(user=user).update(default=False)

    serializer = AddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    utils.log_error(request, f'参数错误:{serializer.errors}')
    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def update(request):
    pk = request.GET.get('id')
    addr = Address.objects.filter(pk=pk).first()
    if not addr:
        return APIResponse(code=1, msg='对象不存在')

    data = request.data
    default = _is_true(data.get('default', False))
    user = data.get('user')

    if default and user:
        Address.objects.filter(user=user).update(default=False)

    serializer = AddressSerializer(addr, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    utils.log_error(request, f'参数错误:{serializer.errors}')
    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def delete(request):
    ids = request.GET.get('ids')
    if not ids:
        return APIResponse(code=1, msg='ids不能为空')

    ids_arr = [s.strip() for s in ids.split(',') if s.strip()]
    Address.objects.filter(id__in=ids_arr).delete()
    return APIResponse(code=0, msg='删除成功')
