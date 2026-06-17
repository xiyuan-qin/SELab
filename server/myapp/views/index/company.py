# Create your views here.
from rest_framework.decorators import api_view

from myapp import utils
from myapp.handler import APIResponse
from myapp.models import Company
from myapp.serializers import CompanySerializer


def _get(request, key, default=None):
    return request.GET.get(key, default)


@api_view(['GET'])
def list_user_company_api(request):
    user_id = _get(request, 'userId')
    if not user_id:
        return APIResponse(code=1, msg='userId不能为空')

    qs = Company.objects.filter(user=user_id)
    return APIResponse(code=0, msg='查询成功', data=CompanySerializer(qs, many=True).data)


@api_view(['POST'])
def create(request):
    user = request.data.get('user')
    if not user:
        return APIResponse(code=1, msg='参数错误')

    if Company.objects.filter(user=user).exists():
        return APIResponse(code=1, msg='已创建过了')

    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    utils.log_error(request, f'参数错误:{serializer.errors}')
    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
def update(request):
    pk = _get(request, 'id', -1)
    company = Company.objects.filter(pk=pk).first()
    if not company:
        return APIResponse(code=1, msg='对象不存在')

    serializer = CompanySerializer(company, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

    utils.log_error(request, f'参数错误:{serializer.errors}')
    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
def delete(request):
    ids = request.GET.get('ids')
    if not ids:
        return APIResponse(code=1, msg='ids不能为空')

    ids_arr = [i.strip() for i in ids.split(',') if i.strip()]
    Company.objects.filter(id__in=ids_arr).delete()
    return APIResponse(code=0, msg='删除成功')
