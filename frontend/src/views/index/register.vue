<template>
  <div class="container">
    <div class="tel-regist-page pc-style">
      <div class="regist-title">
        <span>签下卖身契</span>
        <span @click="router.push({name:'login'})" class="toWxLogin">已入坑？去打卡</span>
      </div>

      <!-- 身份选择 -->
      <div class="role-pick">
        <div class="role-label">选择你的身份</div>
        <div class="role-cards">
          <div
            class="role-card"
            :class="{ active: tData.form.role === 'user' }"
            @click="tData.form.role = 'user'"
          >
            <div class="role-name">我是牛马</div>
            <div class="role-desc">求职者 · 投简历找坑</div>
          </div>
          <div
            class="role-card hr"
            :class="{ active: tData.form.role === 'hr' }"
            @click="tData.form.role = 'hr'"
          >
            <div class="role-name">我是工头</div>
            <div class="role-desc">招聘方 · 发岗位招人</div>
          </div>
        </div>
      </div>

      <div class="regist-padding">
        <div class="common-input">
          <img :src="MailIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="你的工号（邮箱）" v-model="tData.form.username" type="text" class="input">
          </div>
        </div>
      </div>
      <div class="regist-padding">
        <div class="common-input">
          <img :src="PwdIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="设置卖身密码" v-model="tData.form.password" type="password" class="input">
          </div>
        </div>
      </div>
      <div class="regist-padding">
        <div class="common-input">
          <img :src="PwdIcon" class="left-icon">
          <div class="input-view">
            <input placeholder="确认卖身密码" v-model="tData.form.repassword" type="password" class="input" @keyup.enter="handleRegister">
          </div>
        </div>
      </div>
      <div class="tel-login">
        <div class="next-btn-view">
          <button class="next-btn" :class="{ hr: tData.form.role === 'hr' }" @click="handleRegister">
            {{ tData.form.role === 'hr' ? '开张招人' : '签字画押' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import {userRegisterApi} from '/@/api/index/user'
import {message} from "ant-design-vue";
import MailIcon from '/@/assets/images/mail-icon.svg';
import PwdIcon from '/@/assets/images/pwd-icon.svg';

const router = useRouter();

const tData = reactive({
  form: {
    username: '',
    password: '',
    repassword: '',
    role: 'user',
  }
})

const handleRegister = () => {
  if (tData.form.username === '' || tData.form.password === '' || tData.form.repassword === '') {
    message.warn('请完整填写卖身信息')
    return;
  }
  if (tData.form.password !== tData.form.repassword) {
    message.warn('两次密码不一致')
    return;
  }

  userRegisterApi({
    username: tData.form.username,
    password: tData.form.password,
    repassword: tData.form.repassword,
    role: tData.form.role,
  }).then(() => {
    message.success(tData.form.role === 'hr' ? '工头上线！去登录开张吧！' : '恭喜成为一名光荣的牛马！')
    router.push({name: 'login'})
  }).catch((err: any) => {
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
    radial-gradient(ellipse at 20% 20%, rgba(37,99,235,0.12) 0%, transparent 50%);
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pc-style {
  position: relative;
  width: 440px;
  background: var(--nm-dark-2);
  border-radius: var(--nm-radius-lg);
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
    background: linear-gradient(90deg, var(--nm-primary), var(--nm-hr));
  }
}

.tel-regist-page {
  overflow: hidden;

  .regist-title {
    font-size: 16px;
    color: #e7e5e4;
    font-weight: 700;
    line-height: 28px;
    margin: 32px 0 20px;
    padding: 0 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .toWxLogin {
      color: var(--nm-primary);
      cursor: pointer;
      font-size: 13px;
      font-weight: 400;
      transition: color 0.2s;
      &:hover { color: var(--nm-primary-hover); }
    }
  }

  .regist-padding {
    padding: 0 24px;
    margin-bottom: 10px;
  }
}

.role-pick {
  padding: 0 24px 6px;
  .role-label {
    color: #a8a29e;
    font-size: 12px;
    margin-bottom: 10px;
  }
  .role-cards {
    display: flex;
    gap: 12px;
  }
  .role-card {
    flex: 1;
    padding: 12px 14px;
    border: 1px solid var(--nm-dark-3);
    border-radius: var(--nm-radius);
    background: var(--nm-dark);
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;

    .role-name {
      color: #e7e5e4;
      font-size: 15px;
      font-weight: 700;
    }
    .role-desc {
      color: #78716c;
      font-size: 12px;
      margin-top: 4px;
    }

    &.active {
      border-color: var(--nm-primary);
      background: rgba(234,88,12,0.08);
      .role-name { color: var(--nm-primary); }
    }
    &.hr.active {
      border-color: var(--nm-hr);
      background: rgba(37,99,235,0.1);
      .role-name { color: #60a5fa; }
    }
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
      &::placeholder { color: #57534e; }
    }
  }
}

.tel-login {
  padding: 8px 24px 0;
}

.next-btn {
  background: linear-gradient(135deg, var(--nm-primary), #c2410c);
  border-radius: var(--nm-radius);
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

  &.hr {
    background: linear-gradient(135deg, var(--nm-hr), var(--nm-hr-hover));
  }
  &:hover { opacity: 0.92; transform: translateY(-1px); }
  &:active { transform: translateY(0); }
}
</style>
