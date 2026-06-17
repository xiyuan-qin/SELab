# Create your views here.
from rest_framework.decorators import api_view

from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Post
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import PostSerializer


def _qget(request, key, default=None):
    return request.GET.get(key, default)


@api_view(['GET'])
def list_user_post_api(request):
    user_id = _qget(request, 'userId')
    if not user_id:
        return APIResponse(code=1, msg='userId不能为空')

    queryset = Post.objects.filter(user=user_id).order_by('-create_time')
    return APIResponse(code=0, msg='查询成功', data=PostSerializer(queryset, many=True).data)


@api_view(['GET'])
def list_company_post_api(request):
    company_id = _qget(request, 'companyId')
    if not company_id:
        return APIResponse(code=1, msg='companyId不能为空')

    queryset = Post.objects.filter(company=company_id).order_by('-create_time')
    return APIResponse(code=0, msg='查询成功', data=PostSerializer(queryset, many=True).data)


@api_view(['POST'])
def create(request):
    ser = PostSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return APIResponse(code=0, msg='创建成功', data=ser.data)

    # 记录参数错误用于排查
    utils.log_error(request, '参数错误')
    return APIResponse(code=1, msg='创建失败')
