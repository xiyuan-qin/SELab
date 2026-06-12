"""myapp 路由 —— URL 与前端 src/api 中的定义一一对应。

前缀在 server/urls.py 中挂在 /myapp/ 下：
  前台： /myapp/index/...
  后台： /myapp/admin/...
"""
from django.urls import path

from myapp.views import admin, common, thing, user

urlpatterns = [
    # ---------- 前台 用户 ----------
    path('index/user/login', user.login),
    path('index/user/register', user.register),
    path('index/user/info', user.info),
    path('index/user/update', user.update),
    path('index/user/updatePwd', user.update_pwd),

    # ---------- 前台 岗位 ----------
    path('index/thing/list', thing.list_thing),
    path('index/thing/list_user_thing', thing.list_user_thing),
    path('index/thing/detail', thing.detail),
    path('index/thing/create', thing.create),
    path('index/thing/update', thing.update),
    path('index/thing/delete', thing.delete),
    path('index/thing/addWishUser', thing.add_wish_user),
    path('index/thing/removeWishUser', thing.remove_wish_user),
    path('index/thing/addCollectUser', thing.add_collect_user),
    path('index/thing/removeCollectUser', thing.remove_collect_user),
    path('index/thing/getWishThingList', thing.get_wish_thing_list),
    path('index/thing/getCollectThingList', thing.get_collect_thing_list),

    # ---------- 前台 分类 / 公告 ----------
    path('index/classification/list', common.classification_list),
    path('index/notice/list_api', common.notice_list),

    # ---------- 后台 登录 ----------
    path('admin/adminLogin', admin.admin_login),

    # ---------- 后台 用户管理 ----------
    path('admin/user/list', admin.user_list),
    path('admin/user/create', admin.user_create),
    path('admin/user/update', admin.user_update),
    path('admin/user/delete', admin.user_delete),

    # ---------- 后台 概览 ----------
    path('admin/overview/count', admin.overview_count),
    path('admin/overview/sysInfo', admin.overview_sys_info),

    # ---------- 后台 岗位管理 ----------
    path('admin/thing/list', admin.thing_list),
    path('admin/thing/create', admin.thing_create),
    path('admin/thing/update', admin.thing_update),
    path('admin/thing/delete', admin.thing_delete),

    # ---------- 后台 公司管理 ----------
    path('admin/company/list', admin.company_list),
    path('admin/company/create', admin.company_create),
    path('admin/company/update', admin.company_update),
    path('admin/company/delete', admin.company_delete),

    # ---------- 后台 简历管理 ----------
    path('admin/resume/list', admin.resume_list),
    path('admin/resume/update', admin.resume_update),
    path('admin/resume/delete', admin.resume_delete),

    # ---------- 后台 评论管理 ----------
    path('admin/comment/list', admin.comment_list),
    path('admin/comment/delete', admin.comment_delete),

    # ---------- 后台 分类管理 ----------
    path('admin/classification/list', common.classification_list),
    path('admin/classification/create', common.classification_create),
    path('admin/classification/update', common.classification_update),
    path('admin/classification/delete', common.classification_delete),

    # ---------- 后台 公告管理 ----------
    path('admin/notice/list', common.notice_list),
    path('admin/notice/create', common.notice_create),
    path('admin/notice/update', common.notice_update),
    path('admin/notice/delete', common.notice_delete),
]
