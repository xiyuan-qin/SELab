from rest_framework.response import Response


class APIResponse(Response):
    """兼容原有响应结构的简单封装：{code, msg, data, ...}。"""

    def __init__(self, code=0, msg='', data=None, status=200, headers=None, content_type=None, **kwargs):
        payload = {'code': code, 'msg': msg}
        if data is not None:
            payload['data'] = data

        # 合并额外字段（保持与原行为一致，允许覆盖）
        for k, v in kwargs.items():
            payload[k] = v

        super().__init__(data=payload, status=status,
                         template_name=None, headers=headers,
                         exception=False, content_type=content_type)
