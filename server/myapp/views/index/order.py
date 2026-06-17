# Create your views here.
import datetime

from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Order, Thing
from myapp.serializers import OrderSerializer


def _get_q(request, key, default=None):
    return request.GET.get(key, default)


@api_view(['GET'])
def list_api(request):
    user_id = _get_q(request, 'userId', -1)
    status_q = _get_q(request, 'orderStatus', '')

    qs = Order.objects.filter(user=user_id).filter(status__contains=status_q).order_by('-order_time')
    return APIResponse(code=0, msg='查询成功', data=OrderSerializer(qs, many=True).data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):
    payload = request.data.copy()
    user = payload.get('user')
    thing_id = payload.get('thing')
    count = payload.get('count')

    if not user or not thing_id or not count:
        return APIResponse(code=1, msg='参数错误')

    thing = Thing.objects.filter(pk=thing_id).first()
    if not thing:
        return APIResponse(code=1, msg='商品不存在')

    try:
        cnt = int(count)
    except Exception:
        return APIResponse(code=1, msg='参数错误')

    if thing.repertory < cnt:
        return APIResponse(code=1, msg='库存不足')

    payload['create_time'] = datetime.datetime.now()
    payload['order_number'] = str(utils.get_timestamp())
    payload['status'] = '1'

    serializer = OrderSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        # 库存、积分等后续在支付或回调时处理
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    print(serializer.errors)
    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def cancel_order(request):
    pk = _get_q(request, 'id', -1)
    order = Order.objects.filter(pk=pk).first()
    if not order:
        return APIResponse(code=1, msg='对象不存在')

    data = {'status': 7}
    serializer = OrderSerializer(order, data=data)
    if serializer.is_valid():
        serializer.save()
        # 可在此处恢复库存或处理积分逻辑
        return APIResponse(code=0, msg='取消成功', data=serializer.data)

    print(serializer.errors)
    return APIResponse(code=1, msg='更新失败')
