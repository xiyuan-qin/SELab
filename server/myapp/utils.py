import datetime
import hashlib
import time
from typing import List, Dict, Any

from myapp.serializers import ErrorLogSerializer


def get_timestamp() -> int:
    """返回当前毫秒时间戳（整数）。"""
    return int(time.time() * 1000)


def md5value(text: str) -> str:
    """计算给定字符串的 MD5（小写）。"""
    return hashlib.md5(text.encode('utf-8')).hexdigest().lower()


def dict_fetchall(cursor) -> List[Dict[str, Any]]:
    """把数据库 cursor 的结果转换为字典列表。"""
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def get_ip(request) -> str:
    """尽量从请求头中解析客户端 IP（优先 X-Real-IP / X-Forwarded-For）。"""
    x_real = request.META.get('HTTP_X_REAL_IP')
    if x_real:
        return x_real
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def get_ua(request) -> str:
    """返回 User-Agent（最多 200 字符）。"""
    ua = request.META.get('HTTP_USER_AGENT', '')
    return ua[:200]


def getWeekDays() -> List[str]:
    """返回最近 7 天（含今天）的日期列表，格式 'YYYY-MM-DD'，按升序。"""
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    return days


def get_monday() -> str:
    """返回本周周一的日期字符串 'YYYY-MM-DD'。"""
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    return monday.strftime('%Y-%m-%d')


def log_error(request, content) -> None:
    """使用 `ErrorLogSerializer` 保存错误日志（容错地构造载荷）。"""
    payload = {
        'ip': get_ip(request),
        'method': getattr(request, 'method', ''),
        'url': getattr(request, 'path', ''),
        'content': content,
    }
    serializer = ErrorLogSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
