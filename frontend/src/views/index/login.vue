<template>
  <div class="container">
    <div class="login-page pc-style">
      <img :src="LogoIcon" alt="logo" class="logo-icon">
      <div class="login-tab">
        <div class="tab-selected">
          <span>牛马直聘账号登录</span>
          <span class="tabline tabline-width"></span>
        </div>
      </div>
      <div class="mail-login" type="login">
        <div class="common-input">
          <img :src="MailIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="请输入邮箱账号" v-model="pageData.loginForm.username" type="text" class="input">
            <p class="err-view">
            </p>
          </div>
          <!---->
        </div>
        <div class="common-input">
          <img :src="PwdIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="请输入密码" v-model="pageData.loginForm.password" type="password" class="input">
            <p class="err-view">
            </p>
          </div>
<!--          <img src="@/assets/pwd-hidden.svg" class="right-icon">-->
          <!---->
        </div>
        <div class="next-btn-view">
          <button class="next-btn btn-active" style="margin: 16px 0px;" @click="handleLogin">登录牛马直聘</button>
        </div>
      </div>
      <div class="test-account-box">
        <div class="test-title">前端测试账号</div>
        <div class="test-row">
          <span>普通用户：`user / 123`</span>
          <button class="quick-fill-btn" @click="fillTestAccount('user')">一键填充</button>
        </div>
        <div class="test-row">
          <span>管理员：`admin / 123`</span>
          <button class="quick-fill-btn" @click="fillTestAccount('admin')">一键填充</button>
        </div>
      </div>
      <div class="operation">
        <a @click="handleCreateUser" class="forget-pwd" style="text-align: left;">注册新账号</a>
        <a class="forget-pwd" style="text-align: right;">忘记密码？</a>
      </div>
      <div class="quick-route-box">
        <button class="quick-route-btn" @click="quickJump('portal')">去首页</button>
        <button class="quick-route-btn" @click="quickJump('search')">去搜索页</button>
        <button class="quick-route-btn" @click="quickJump('usercenter')">去个人中心</button>
        <button class="quick-route-btn" @click="quickJump('adminLogin')">去管理员登录</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {useUserStore} from '/@/store';
import {message} from "ant-design-vue";
import LogoIcon from '/@/assets/images/k-logo.png';
import MailIcon from '/@/assets/images/mail-icon.svg';
import PwdIcon from '/@/assets/images/pwd-icon.svg';
import { ADMIN_USER_ID, ADMIN_USER_NAME, ADMIN_USER_TOKEN, USER_ID, USER_NAME, USER_TOKEN } from '/@/store/constants';


const router = useRouter();
const userStore = useUserStore();

const pageData = reactive({
  loginForm: {
    username: '',
    password: ''
  }
})

const applyFrontendTestLogin = (type: 'user' | 'admin') => {
  if (type === 'admin') {
    userStore.$patch((state) => {
      state.admin_user_id = 'admin-test-id'
      state.admin_user_name = 'admin'
      state.admin_user_token = 'admin-test-token'
    })
    localStorage.setItem(ADMIN_USER_ID, 'admin-test-id')
    localStorage.setItem(ADMIN_USER_NAME, 'admin')
    localStorage.setItem(ADMIN_USER_TOKEN, 'admin-test-token')
    message.success('管理员测试账号登录成功（前端模式）')
    router.push({ name: 'portal' })
    return
  }

  userStore.$patch((state) => {
    state.user_id = 'user-test-id'
    state.user_name = 'user'
    state.user_token = 'user-test-token'
  })
  localStorage.setItem(USER_ID, 'user-test-id')
  localStorage.setItem(USER_NAME, 'user')
  localStorage.setItem(USER_TOKEN, 'user-test-token')
  message.success('用户测试账号登录成功（前端模式）')
  router.push({ name: 'portal' })
}

const handleLogin = ()=> {
  if (pageData.loginForm.username === 'user' && pageData.loginForm.password === '123') {
    applyFrontendTestLogin('user')
    return
  }
  if (pageData.loginForm.username === 'admin' && pageData.loginForm.password === '123') {
    applyFrontendTestLogin('admin')
    return
  }

  userStore.login({
    username: pageData.loginForm.username,
    password: pageData.loginForm.password
  }).then(res=> {
    loginSuccess()
    console.log('success==>', userStore.user_name)
    console.log('success==>', userStore.user_id)
    console.log('success==>', userStore.user_token)
  }).catch(err => {
    message.warn(err.msg || '登录失败，请检查账号密码')
  })
}

const handleCreateUser = () => {
  router.push({name:'register'})
}

const fillTestAccount = (type: 'user' | 'admin') => {
  if (type === 'admin') {
    pageData.loginForm.username = 'admin'
    pageData.loginForm.password = '123'
    message.info('已填充管理员测试账号：admin / 123')
    return
  }
  pageData.loginForm.username = 'user'
  pageData.loginForm.password = '123'
  message.info('已填充用户测试账号：user / 123')
}

const quickJump = (target: 'portal' | 'search' | 'usercenter' | 'adminLogin') => {
  if (target === 'portal') {
    router.push({ name: 'portal' })
    return
  }
  if (target === 'search') {
    router.push({ name: 'search', query: { keyword: '前端' } })
    return
  }
  if (target === 'adminLogin') {
    router.push({ name: 'adminLogin' })
    return
  }
  if (!localStorage.getItem(USER_TOKEN)) {
    applyFrontendTestLogin('user')
  }
  router.push({ name: 'userInfoEditView' })
}

const loginSuccess= ()=> {
  router.push({ name: 'portal' })
  message.success('登录成功，欢迎来到牛马直聘！')
}


</script>
<style scoped lang="less">
div {
  display: block;
}

.container {
  //background-color: #f1f1f1;
  background-image: url('../images/admin-login-bg.jpg');
  background-size: cover;
  object-fit: cover;
  height: 100%;
  max-width: 100%;
  display:flex;
  justify-content: center;
  align-items:center;
}

.new-content {
  position: absolute;
  left: 0;
  right: 0;
  margin: 80px auto 0;
  width: 980px;
}

.logo-img {
  width: 125px;
  display: block;
  margin-left: 137.5px;
}

.login-page {
  overflow: hidden;
  background: #fff;

  .logo-icon {
    margin-top: 20px;
    margin-left: 175px;
    width: 48px;
    height: 48px;
  }
}

.pc-style {
  position: relative;
  width: 400px;
  min-height: 520px;
  background: #fff;
  border-radius: 4px;
  -webkit-box-shadow: 2px 2px 6px #aaa;
  box-shadow: 2px 2px 6px #aaa;
}

.login-tab {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  color: #1e1e1e;
  font-size: 14px;
  color: #1e1e1e;
  font-weight: 500;
  height: 46px;
  line-height: 44px;
  margin-bottom: 40px;
  border-bottom: 1px solid #c3c9d5;

  div {
    position: relative;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    text-align: center;
    cursor: pointer;
  }

  .tabline {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 0 auto;
    display: inline-block;
    width: 0;
    height: 2px;
    background: #3d5b96;
    -webkit-transition: width .5s cubic-bezier(.46, 1, .23, 1.52);
    transition: width .5s cubic-bezier(.46, 1, .23, 1.52);
  }

  tab-selected {
    color: #1e1e1e;
    font-weight: 500;
  }

  .mail-login, .tel-login {
    padding: 0 28px;
  }

}

.mail-login {
  margin: 0px 24px;
}

.common-input {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: start;
  -ms-flex-align: start;
  align-items: flex-start;

  .left-icon {
    margin-right: 12px;
    width: 24px;
  }

  .input-view {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;

    .input {
      font-weight: 500;
      font-size: 14px;
      color: #1e1e1e;
      height: 26px;
      line-height: 26px;
      border: none;
      padding: 0;
      display: block;
      width: 100%;
      letter-spacing: 1.5px;
    }

    err-view {
      margin-top: 4px;
      height: 16px;
      line-height: 16px;
      font-size: 12px;
      color: #f62a2a;
    }
  }
}

.next-btn {
  background: var(--nm-primary);
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  height: 40px;
  line-height: 40px;
  text-align: center;
  width: 100%;
  outline: none;
  cursor: pointer;
}

button {
  background: transparent;
  padding: 0;
  border-width: 0px;
}

button, input, select, textarea {
  margin: 0;
  padding: 0;
  outline: none;
}

.operation {
  display: flex;
  flex-direction: row;
  margin: 0 24px;
}

.forget-pwd {
  //text-align: center;
  display: block;
  overflow: hidden;
  flex:1;
  margin: 0 auto;
  color: var(--nm-primary);
  font-size: 14px;
  cursor: pointer;
}

.test-account-box {
  margin: 8px 24px 0;
  padding: 10px 12px;
  border: 1px dashed var(--nm-border);
  border-radius: var(--nm-radius-sm);
  background: var(--nm-bg-soft);

  .test-title {
    font-size: 13px;
    font-weight: 600;
    color: var(--nm-text-main);
    margin-bottom: 6px;
  }

  .test-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 12px;
    color: var(--nm-text-sub);
    margin-top: 4px;
  }
}

.quick-fill-btn {
  border: 1px solid var(--nm-primary);
  color: var(--nm-primary);
  background: #fff;
  border-radius: var(--nm-radius-sm);
  padding: 2px 8px;
  font-size: 12px;
  cursor: pointer;
}

.quick-route-box {
  margin: 10px 24px 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.quick-route-btn {
  border: 1px solid var(--nm-border);
  color: var(--nm-text-main);
  background: #fff;
  border-radius: var(--nm-radius-sm);
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
}

</style>
