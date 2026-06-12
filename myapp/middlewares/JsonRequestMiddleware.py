"""请求体兼容中间件 —— 在 settings.MIDDLEWARE 中以
`myapp.middlewares.JsonRequestMiddleware.JsonRequest` 引用。

前端各接口的 Content-Type 不统一（有的 multipart/form-data，有的 application/json）。
Django 的 request.POST 只解析表单编码，遇到 JSON body 时为空，会触发“字段为空”类误报。

本中间件在请求进入视图前，把 application/json 的请求体解析出来填进 request.POST，
使所有视图无需改动即可同时兼容 JSON 与表单两种提交方式。
"""
import json

from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin


class JsonRequest(MiddlewareMixin):
    def process_request(self, request):
        if request.method not in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return
        if 'application/json' not in (request.content_type or ''):
            return
        if not request.body:
            return
        try:
            data = json.loads(request.body)
        except (ValueError, TypeError):
            return
        if not isinstance(data, dict):
            return

        q = QueryDict('', mutable=True)
        for key, value in data.items():
            # 列表值用 setlist，标量统一转成字符串，贴合 request.POST 的取值习惯
            if isinstance(value, (list, tuple)):
                q.setlist(key, [str(v) for v in value])
            elif value is None:
                q[key] = ''
            else:
                q[key] = str(value)
        request.POST = q
