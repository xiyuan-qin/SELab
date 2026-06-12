<template>
  <a-layout class="admin-layout">
    <a-layout-sider :width="220" class="sider">
      <div class="logo">牛马直聘 · 后台</div>
      <a-menu
        :selectedKeys="selectedKeys"
        mode="inline"
        theme="dark"
        @click="onMenuClick"
      >
        <a-menu-item key="overview">数据概览</a-menu-item>
        <a-menu-item-group title="招聘管理">
          <a-menu-item key="thing">岗位管理</a-menu-item>
          <a-menu-item key="company">公司管理</a-menu-item>
          <a-menu-item key="resume">简历管理</a-menu-item>
          <a-menu-item key="comment">评论管理</a-menu-item>
        </a-menu-item-group>
        <a-menu-item-group title="系统管理">
          <a-menu-item key="user">用户管理</a-menu-item>
          <a-menu-item key="classification">分类管理</a-menu-item>
          <a-menu-item key="tag">标签管理</a-menu-item>
          <a-menu-item key="ad">广告管理</a-menu-item>
          <a-menu-item key="notice">公告管理</a-menu-item>
        </a-menu-item-group>
        <a-menu-item-group title="日志与信息">
          <a-menu-item key="loginLog">登录日志</a-menu-item>
          <a-menu-item key="opLog">操作日志</a-menu-item>
          <a-menu-item key="errorLog">错误日志</a-menu-item>
          <a-menu-item key="sysInfo">系统信息</a-menu-item>
        </a-menu-item-group>
      </a-menu>
    </a-layout-sider>

    <a-layout>
      <a-layout-header class="header">
        <span class="page-title">{{ currentTitle }}</span>
        <div class="header-right">
          <span class="admin-name">{{ adminName }}</span>
          <a-button type="link" @click="handleLogout">退出登录</a-button>
        </div>
      </a-layout-header>
      <a-layout-content class="content">
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ADMIN_USER_ID, ADMIN_USER_NAME, ADMIN_USER_TOKEN } from '/@/store/constants';

const route = useRoute();
const router = useRouter();

const TITLES: Record<string, string> = {
  overview: '数据概览',
  thing: '岗位管理',
  company: '公司管理',
  resume: '简历管理',
  comment: '评论管理',
  user: '用户管理',
  classification: '分类管理',
  tag: '标签管理',
  ad: '广告管理',
  notice: '公告管理',
  loginLog: '登录日志',
  opLog: '操作日志',
  errorLog: '错误日志',
  sysInfo: '系统信息',
};

const selectedKeys = computed(() => [route.name as string]);
const currentTitle = computed(() => TITLES[route.name as string] || '管理后台');
const adminName = computed(() => localStorage.getItem(ADMIN_USER_NAME) || '管理员');

const onMenuClick = ({ key }: { key: string }) => {
  if (key !== route.name) router.push({ name: key });
};

const handleLogout = () => {
  localStorage.removeItem(ADMIN_USER_ID);
  localStorage.removeItem(ADMIN_USER_NAME);
  localStorage.removeItem(ADMIN_USER_TOKEN);
  router.push({ name: 'adminLogin' });
};
</script>

<style scoped lang="less">
.admin-layout {
  height: 100vh;
}
.sider {
  background: #001529;
  overflow-y: auto;
}
.logo {
  height: 56px;
  line-height: 56px;
  text-align: center;
  color: #fff;
  font-weight: 700;
  letter-spacing: 1px;
  background: rgba(255, 255, 255, 0.04);
}
.header {
  background: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  .page-title {
    font-size: 16px;
    font-weight: 600;
    color: #1f2937;
  }
  .header-right {
    display: flex;
    align-items: center;
    gap: 8px;
    .admin-name {
      color: #6b7280;
      font-size: 14px;
    }
  }
}
.content {
  margin: 16px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  overflow-y: auto;
}
</style>
