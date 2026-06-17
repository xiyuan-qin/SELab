from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from myapp.models import User


# 后台接口认证（管理员/演示帐号）
class AdminTokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_ADMINTOKEN')
        if not token:
            raise exceptions.AuthenticationFailed('AUTH_FAIL_END')

        print(f'检查 adminToken => {token}')
        user = User.objects.filter(admin_token=token).first()
        # 条件：必须存在该用户，且 role 不是 '2'（表示禁止的角色）
        if not user or getattr(user, 'role', None) == '2':
            raise exceptions.AuthenticationFailed('AUTH_FAIL_END')

        print('adminToken 验证通过')


# 前台接口认证（普通用户）
class TokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            print('检查 token => 为空')
            raise exceptions.AuthenticationFailed('AUTH_FAIL_FRONT')

        print(f'检查 token => {token}')
        user = User.objects.filter(token=token).first()
        # 条件：必须存在该用户，且 role 不是 '1' 或 '3'（非普通用户）
        if not user or getattr(user, 'role', None) in ['1', '3']:
            raise exceptions.AuthenticationFailed('AUTH_FAIL_FRONT')

        print('token 验证通过')
