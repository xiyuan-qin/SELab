<template>
  <div class="container">
    <div class="login-page pc-style">
      <img :src="LogoIcon" alt="logo" class="logo-icon">
      <div class="login-tab">
        <div class="tab-selected">
          <span>欢迎归来，社畜</span>
          <span class="tabline tabline-width"></span>
        </div>
      </div>
      <div class="mail-login" type="login">
        <div class="common-input">
          <img :src="MailIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="你的工号（邮箱）" v-model="pageData.loginForm.username" type="text" class="input">
            <p class="err-view">
            </p>
          </div>
          <!---->
        </div>
        <div class="common-input">
          <img :src="PwdIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="你的密码（忘了说明摸鱼太久了）" v-model="pageData.loginForm.password" type="password" class="input">
            <p class="err-view">
            </p>
          </div>
<!--          <img src="@/assets/pwd-hidden.svg" class="right-icon">-->
          <!---->
        </div>
        <div class="next-btn-view">
          <button class="next-btn btn-active" style="margin: 16px 0px;" @click="handleLogin">打卡上工</button>
        </div>
      </div>
      <div class="test-account-box">
        <div class="test-title">摸鱼测试通道</div>
        <div class="test-row">
          <span>普通牛马：`user / 123`</span>
          <button class="quick-fill-btn" @click="fillTestAccount('user')">一键填充</button>
        </div>
        <div class="test-row">
          <span>大老板：`admin / 123`</span>
          <button class="quick-fill-btn" @click="fillTestAccount('admin')">一键填充</button>
        </div>
      </div>
      <div class="operation">
        <a @click="handleCreateUser" class="forget-pwd" style="text-align: left;">还没入坑？点这里</a>
        <a class="forget-pwd" style="text-align: right;">忘了密码？</a>
      </div>
      <div class="quick-route-box">
        <button class="quick-route-btn" @click="quickJump('portal')">去牛马市场</button>
        <button class="quick-route-btn" @click="quickJump('search')">去找下一个坑</button>
        <button class="quick-route-btn" @click="quickJump('usercenter')">查看我的坑况</button>
        <button class="quick-route-btn" @click="quickJump('adminLogin')">老板登录入口</button>
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
    message.success('老板模式开启，开始压榨！')
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
  message.success('牛马模式开启，加油干！')
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
    message.warn(err.msg || '打卡失败，账号密码检查一下')
  })
}

const handleCreateUser = () => {
  router.push({name:'register'})
}

const fillTestAccount = (type: 'user' | 'admin') => {
  if (type === 'admin') {
    pageData.loginForm.username = 'admin'
    pageData.loginForm.password = '123'
    message.info('已填充大老板账号：admin / 123，准备压榨')
    return
  }
  pageData.loginForm.username = 'user'
  pageData.loginForm.password = '123'
  message.info('已填充牛马账号：user / 123，准备上工')
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
  message.success('打卡成功，社畜加油！今天也要元气满满地搬砖！')
}


</script>
<style scoped lang="less">
div {
  display: block;
}

.container {
  background: var(--nm-dark);
  background-image:
    radial-gradient(ellipse at 20% 50%, rgba(234,88,12,0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(220,38,38,0.1) 0%, transparent 50%),
    radial-gradient(ellipse at 60% 80%, rgba(234,88,12,0.08) 0%, transparent 50%);
  height: 100%;
  max-width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;

  // 装饰性大字
  &::before {
    content: '牛马直聘';
    position: absolute;
    font-size: 180px;
    font-weight: 900;
    color: rgba(234,88,12,0.04);
    letter-spacing: -8px;
    pointer-events: none;
    user-select: none;
    white-space: nowrap;
  }
}

.login-page {
  overflow: hidden;
  background: var(--nm-dark-2);
  border: 1px solid var(--nm-dark-3);
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--nm-primary), var(--nm-accent));
  }

  .logo-icon {
    margin-top: 24px;
    margin-left: 175px;
    width: 44px;
    height: 44px;
    filter: brightness(0) invert(1);
    opacity: 0.9;
  }
}

.pc-style {
  position: relative;
  width: 420px;
  min-height: 520px;
  background: var(--nm-dark-2);
  border-radius: var(--nm-radius);
  box-shadow: 0 24px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(234,88,12,0.2);
}

.login-tab {
  display: flex;
  color: #e7e5e4;
  font-size: 15px;
  font-weight: 600;
  height: 52px;
  line-height: 50px;
  margin-bottom: 32px;
  border-bottom: 1px solid var(--nm-dark-3);

  div {
    position: relative;
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
    background: var(--nm-primary);
    transition: width .4s cubic-bezier(.46, 1, .23, 1.52);
  }

  .tabline-width {
    width: 32px;
  }
}

.mail-login {
  margin: 0 24px;
}

.common-input {
  display: flex;
  align-items: center;
  background: var(--nm-dark-3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--nm-radius-sm);
  padding: 10px 14px;
  margin-bottom: 12px;
  transition: border-color 0.2s;

  &:focus-within {
    border-color: var(--nm-primary);
    background: rgba(234,88,12,0.05);
  }

  .left-icon {
    margin-right: 10px;
    width: 18px;
    opacity: 0.5;
    filter: brightness(0) invert(1);
    flex-shrink: 0;
  }

  .input-view {
    flex: 1;

    .input {
      font-weight: 400;
      font-size: 14px;
      color: #e7e5e4;
      height: 24px;
      line-height: 24px;
      border: none;
      padding: 0;
      display: block;
      width: 100%;
      letter-spacing: 0.5px;
      background: transparent;

      &::placeholder {
        color: #57534e;
        font-weight: 400;
      }
    }
  }
}

.next-btn {
  background: linear-gradient(135deg, var(--nm-primary), #c2410c);
  border-radius: var(--nm-radius-sm);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  height: 44px;
  line-height: 44px;
  text-align: center;
  width: 100%;
  outline: none;
  cursor: pointer;
  letter-spacing: 2px;
  border: none;
  transition: opacity 0.2s, transform 0.1s;

  &:hover {
    opacity: 0.9;
    transform: translateY(-1px);
  }
  &:active {
    transform: translateY(0);
  }
}

button {
  background: transparent;
  padding: 0;
  border-width: 0;
}

button, input, select, textarea {
  margin: 0;
  padding: 0;
  outline: none;
}

.next-btn-view {
  margin-top: 8px;
}

.operation {
  display: flex;
  flex-direction: row;
  margin: 12px 24px 0;
}

.forget-pwd {
  display: block;
  overflow: hidden;
  flex: 1;
  color: #78716c;
  font-size: 13px;
  cursor: pointer;
  transition: color 0.2s;

  &:hover {
    color: var(--nm-primary);
  }
}

.test-account-box {
  margin: 16px 24px 0;
  padding: 12px 14px;
  border: 1px dashed rgba(234,88,12,0.3);
  border-radius: var(--nm-radius-sm);
  background: rgba(234,88,12,0.06);

  .test-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--nm-primary);
    margin-bottom: 8px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }

  .test-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 12px;
    color: #78716c;
    margin-top: 6px;
    font-family: 'Courier New', monospace;
  }
}

.quick-fill-btn {
  border: 1px solid var(--nm-primary);
  color: var(--nm-primary);
  background: transparent;
  border-radius: var(--nm-radius-sm);
  padding: 2px 10px;
  font-size: 11px;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;

  &:hover {
    background: var(--nm-primary);
    color: #fff;
  }
}

.quick-route-box {
  margin: 12px 24px 20px;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.quick-route-btn {
  border: 1px solid var(--nm-dark-3);
  color: #78716c;
  background: transparent;
  border-radius: var(--nm-radius-sm);
  padding: 4px 10px;
  font-size: 11px;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;

  &:hover {
    border-color: var(--nm-primary);
    color: var(--nm-primary);
  }
}
</style>
