from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Notice
from myapp.serializers import NoticeSerializer


@api_view(['GET'])
def list_api(request):
    qs = Notice.objects.all().order_by('-create_time')
    return APIResponse(code=0, msg='查询成功', data=NoticeSerializer(qs, many=True).data)

