"""操作日志中间件 —— 在 settings.MIDDLEWARE 中以
`myapp.middlewares.LogMiddleware.OpLogs` 引用。

记录非 GET 的写操作到 OpLog 表，便于后台审计。
"""
import time

from django.utils.deprecation import MiddlewareMixin


class OpLogs(MiddlewareMixin):
    # 不记录这些前缀，避免噪音
    SKIP_PREFIXES = ('/admin/', '/static/', '/upload/', '/favicon.ico')

    def process_request(self, request):
        request._op_start = time.time()

    def process_response(self, request, response):
        try:
            path = request.path
            if request.method == 'GET':
                return response
            if any(path.startswith(p) for p in self.SKIP_PREFIXES):
                return response

            # 延迟导入，避免应用尚未就绪时出错
            from myapp.models import OpLog
            from myapp.utils import get_client_ip

            cost = ''
            if hasattr(request, '_op_start'):
                cost = '%.0f' % ((time.time() - request._op_start) * 1000)

            OpLog.objects.create(
                re_ip=get_client_ip(request),
                re_url=path,
                re_method=request.method,
                re_content=path.rsplit('/', 1)[-1],
                access_time=cost,
            )
        except Exception:
            # 日志失败绝不能影响主流程
            pass
        return response
