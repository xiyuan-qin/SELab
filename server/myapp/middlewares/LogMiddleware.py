# -*- coding:utf-8 -*-
import time
import json

from django.utils.deprecation import MiddlewareMixin

from myapp import utils
from myapp.serializers import OpLogSerializer


class OpLogs(MiddlewareMixin):
    """记录每次请求的基本信息并在响应时保存耗时到数据库。"""

    def process_request(self, request):
        # 在请求对象上保存开始时间和初始元信息，避免中间件实例属性竞争
        request._oplog_start = time.time()
        meta = {
            're_url': request.path,
            're_method': request.method,
            're_ip': utils.get_ip(request),
        }

        # 尝试序列化请求参数（可选）
        try:
            params = request.GET.dict() if request.method == 'GET' else request.POST.dict()
            if params:
                meta['re_content'] = json.dumps(params, ensure_ascii=False)
        except Exception:
            # 保持容错，不影响主流程
            pass

        request._oplog_meta = meta

    def process_response(self, request, response):
        start = getattr(request, '_oplog_start', None)
        meta = getattr(request, '_oplog_meta', None)
        if start is not None and isinstance(meta, dict):
            meta['access_time'] = int((time.time() - start) * 1000)
            serializer = OpLogSerializer(data=meta)
            if serializer.is_valid():
                serializer.save()

        return response
