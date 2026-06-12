<template>
  <div class="admin-login">
    <div class="login-card">
      <div class="brand">
        <span class="brand-title">牛马直聘</span>
        <span class="brand-sub">运营管理后台</span>
      </div>
      <a-form layout="vertical" @submit.prevent="handleLogin">
        <a-form-item label="管理员账号">
          <a-input v-model:value="form.username" size="large" placeholder="请输入账号" @pressEnter="handleLogin" />
        </a-form-item>
        <a-form-item label="密码">
          <a-input-password v-model:value="form.password" size="large" placeholder="请输入密码" @pressEnter="handleLogin" />
        </a-form-item>
        <a-button type="primary" size="large" block :loading="loading" @click="handleLogin">登录</a-button>
      </a-form>
      <p class="tip">默认管理员：admin / 123</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { loginApi } from '/@/api/admin/user';
import { ADMIN_USER_ID, ADMIN_USER_NAME, ADMIN_USER_TOKEN } from '/@/store/constants';

const router = useRouter();
const loading = ref(false);
const form = reactive({ username: 'admin', password: '' });

const handleLogin = () => {
  if (!form.username || !form.password) {
    message.warn('请输入账号和密码');
    return;
  }
  loading.value = true;
  loginApi({ username: form.username, password: form.password })
    .then((res) => {
      localStorage.setItem(ADMIN_USER_ID, res.data.id);
      localStorage.setItem(ADMIN_USER_NAME, res.data.username);
      localStorage.setItem(ADMIN_USER_TOKEN, res.data.admin_token);
      message.success('登录成功');
      router.push({ name: 'overview' });
    })
    .catch((err) => message.error(err.msg || '登录失败'))
    .finally(() => (loading.value = false));
};
</script>

<style scoped lang="less">
.admin-login {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}
.login-card {
  width: 380px;
  padding: 40px 36px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.35);
}
.brand {
  text-align: center;
  margin-bottom: 28px;
  .brand-title {
    display: block;
    font-size: 26px;
    font-weight: 700;
    color: #ea580c;
    letter-spacing: 2px;
  }
  .brand-sub {
    display: block;
    margin-top: 6px;
    font-size: 13px;
    color: #6b7280;
  }
}
.tip {
  margin-top: 16px;
  text-align: center;
  font-size: 12px;
  color: #9ca3af;
}
</style>
