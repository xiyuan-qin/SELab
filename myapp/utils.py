"""通用工具：统一响应格式 + token 生成

前端约定的响应信封：{ code, msg, data }，code == 0 表示成功。
"""
import uuid

from django.http import JsonResponse


def success(data=None, msg='success'):
    return JsonResponse({'code': 0, 'msg': msg, 'data': data}, json_dumps_params={'ensure_ascii': False})


def error(msg='error', code=-1, data=None):
    return JsonResponse({'code': code, 'msg': msg, 'data': data}, json_dumps_params={'ensure_ascii': False})


def make_token():
    return uuid.uuid4().hex


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'mobile': user.mobile,
        'email': user.email,
        'gender': user.gender,
        'description': user.description,
        'role': user.role,
        'score': user.score,
        'status': user.status,
        'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S') if user.create_time else None,
    }


def thing_to_dict(thing):
    return {
        'id': thing.id,
        'title': thing.title,
        'cover': thing.cover,
        'description': thing.description,
        'salary': thing.salary,
        'classification_id': thing.classification_id,
        'classification_title': thing.classification.title if thing.classification else None,
        'company_id': thing.company_id,
        'company_name': thing.company.name if thing.company else None,
        'status': thing.status,
        'browse_count': thing.browse_count,
        'wish_count': thing.wish_count,
        'collect_count': thing.collect_count,
        'comment_count': thing.comment_count,
        'tags': [t.title for t in thing.tags.all()],
        'create_time': thing.create_time.strftime('%Y-%m-%d %H:%M:%S') if thing.create_time else None,
    }
