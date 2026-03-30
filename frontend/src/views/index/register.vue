<template>
  <div class="container">

    <div class="tel-regist-page pc-style">
      <div class="regist-title">
        <span>签下卖身契</span>
        <span @click="router.push({name:'login'})" class="toWxLogin">已入坑？</span>
      </div>

      <div class="regist-padding">
        <div class="common-input">
          <img :src="MailIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="你的工号（邮箱）" v-model="tData.loginForm.username" type="text" class="input">
            <p class="err-view">
            </p>
          </div>
        </div>
      </div>
      <div class="regist-padding">
        <div class="common-input">
          <img :src="PwdIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="设置卖身密码" v-model="tData.loginForm.password" type="password" class="input">
            <p class="err-view">
            </p>
          </div>
        </div>
      </div>
      <div class="regist-padding">
        <div class="common-input">
          <img :src="PwdIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="确认卖身密码" v-model="tData.loginForm.repassword" type="password" class="input">
            <p class="err-view">
            </p>
          </div>
        </div>
      </div>
      <div class="tel-login">
        <div class="next-btn-view">
          <button class="next-btn" @click="handleRegister">签字画押</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {userRegisterApi} from '/@/api/index/user'
import {message} from "ant-design-vue";
import MailIcon from '/@/assets/images/mail-icon.svg';
import PwdIcon from '/@/assets/images/pwd-icon.svg';

const router = useRouter();

const tData = reactive({
  loginForm: {
    username: '',
    password: '',
    repassword: ''
  }
})

const handleRegister = () => {
  console.log('login')
  if(tData.loginForm.username === ''
    || tData.loginForm.password === ''
    || tData.loginForm.repassword === ''){
    message.warn('请完整填写卖身信息')
    return;
  }

  userRegisterApi({
    username: tData.loginForm.username,
    password: tData.loginForm.password,
    repassword: tData.loginForm.repassword
  }).then(res => {
    message.success('恭喜成为一名光荣的牛马！卖身契已生效！')
    router.push({name: 'login'})
  }).catch(err => {
    message.error(err.msg || '入坑失败，请稍后再试')
  })
}


</script>

<style scoped lang="less">
div {
  display: block;
}

.container {
  max-width: 100%;
  background: var(--nm-dark);
  background-image:
    radial-gradient(ellipse at 80% 50%, rgba(234,88,12,0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 20% 20%, rgba(220,38,38,0.1) 0%, transparent 50%);
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pc-style {
  position: relative;
  width: 420px;
  background: var(--nm-dark-2);
  border-radius: var(--nm-radius);
  box-shadow: 0 24px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(234,88,12,0.2);
  overflow: hidden;
  padding-bottom: 32px;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--nm-primary), var(--nm-accent));
  }
}

.tel-regist-page {
  overflow: hidden;

  .regist-title {
    font-size: 16px;
    color: #e7e5e4;
    font-weight: 700;
    line-height: 28px;
    margin: 32px 0 24px;
    padding: 0 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .toWxLogin {
      color: var(--nm-primary);
      float: right;
      cursor: pointer;
      font-size: 13px;
      font-weight: 400;
      transition: color 0.2s;
      &:hover {
        color: var(--nm-primary-hover);
      }
    }
  }

  .regist-padding {
    padding: 0 24px;
    margin-bottom: 10px;
  }
}

.common-input {
  display: flex;
  align-items: center;
  background: var(--nm-dark-3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--nm-radius-sm);
  padding: 10px 14px;
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

    .err-view {
      margin-top: 4px;
      height: 16px;
      line-height: 16px;
      font-size: 12px;
      color: #f87171;
    }
  }
}

.tel-login {
  padding: 4px 24px 0;
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
  border: none;
  letter-spacing: 2px;
  transition: opacity 0.2s, transform 0.1s;

  &:hover {
    opacity: 0.9;
    transform: translateY(-1px);
  }
  &:active {
    transform: translateY(0);
  }
}
</style>
