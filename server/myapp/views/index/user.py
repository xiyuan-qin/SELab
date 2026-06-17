# Create your views here.
import datetime

from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import User
from myapp.serializers import UserSerializer, LoginLogSerializer
from myapp.utils import md5value


def make_login_log(request):
    username = request.data.get('username')
    if not username:
        return

    payload = {
        'username': username,
        'ip': utils.get_ip(request),
        'ua': utils.get_ua(request),
    }
    serializer = LoginLogSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = utils.md5value(request.data.get('password', ''))

    user = User.objects.filter(username=username, password=password).first()
    if not user:
        return APIResponse(code=1, msg='用户名或密码错误')

    if user.role in ['1', '3']:
        return APIResponse(code=1, msg='该帐号为后台管理员帐号')

    update_data = {
        'username': username,
        'password': password,
        'token': md5value(username),
    }
    serializer = UserSerializer(user, data=update_data)
    if serializer.is_valid():
        serializer.save()
        make_login_log(request)
        return APIResponse(code=0, msg='登录成功', data=serializer.data)

    print(serializer.errors)
    return APIResponse(code=1, msg='用户名或密码错误')


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    repassword = request.data.get('repassword')

    if not username or not password or not repassword:
        return APIResponse(code=1, msg='用户名或密码不能为空')
    if password != repassword:
        return APIResponse(code=1, msg='密码不一致')
    if User.objects.filter(username=username).exists():
        return APIResponse(code=1, msg='该用户名已存在')

    data = {
        'username': username,
        'password': utils.md5value(password),
        'role': 2,
        'status': 0,
    }
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    print(serializer.errors)
    return APIResponse(code=1, msg='创建失败')


@api_view(['GET'])
def info(request):
    pk = request.GET.get('id', -1)
    user = User.objects.get(pk=pk)
    return APIResponse(code=0, msg='查询成功', data=UserSerializer(user).data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def update(request):
    pk = request.GET.get('id', -1)
    user = User.objects.filter(pk=pk).first()
    if not user:
        return APIResponse(code=1, msg='对象不存在')

    data = request.data.copy()
    for forbidden in ('username', 'password', 'role'):
        data.pop(forbidden, None)

    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    print(serializer.errors)
    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def updatePwd(request):
    pk = request.GET.get('id', -1)
    user = User.objects.filter(pk=pk).first()
    if not user:
        return APIResponse(code=1, msg='对象不存在')

    if user.role != '2':
        return APIResponse(code=1, msg='参数非法')

    password = request.data.get('password')
    new1 = request.data.get('newPassword1')
    new2 = request.data.get('newPassword2')

    if not password or not new1 or not new2:
        return APIResponse(code=1, msg='不能为空')

    if user.password != utils.md5value(password):
        return APIResponse(code=1, msg='原密码不正确')

    if new1 != new2:
        return APIResponse(code=1, msg='两次密码不一致')

    data = request.data.copy()
    data['password'] = utils.md5value(new1)
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    print(serializer.errors)
    return APIResponse(code=1, msg='更新失败')