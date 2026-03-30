<template>
  <div class="main-bar-view">
    <div class="logo">
      <img :src="logoImage" class="search-icon" @click="$router.push({name:'portal'})">
    </div>
    <div class="search-entry">
      <img :src="SearchIcon" class="search-icon">
      <input placeholder="搜索下一个坑..." ref="keywordRef" @keyup.enter="search" />
    </div>
    <div class="right-view">
      <a style="font-size:16px;line-height: 32px;" @click="handleZhaoren">我要压榨牛马</a>
      <template v-if="userStore.user_token">
        <a-dropdown>
          <a class="ant-dropdown-link" @click="e => e.preventDefault()">
            <img :src="AvatarIcon" class="self-img" >
          </a>
          <template #overlay>
            <a-menu>
              <a-menu-item>
                <a @click="goUserCenter('resumeEditView')">我的卖身契</a>
              </a-menu-item>
              <a-menu-item>
                <a @click="goUserCenter('userInfoEditView')">牛马设置</a>
              </a-menu-item>
              <a-menu-item>
                <a @click="quit()">提桶跑路</a>
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
        <!--        <div class="right-icon">-->
        <!--          <img src="@/assets/cart-icon.svg">-->
        <!--          <span>3</span>-->
        <!--        </div>-->
      </template>
      <template v-else>
        <button class="login btn hidden-sm" @click="goLogin()">入坑打卡</button>
      </template>

      <div class="right-icon" @click="msgVisible=true">
        <img :src="MessageIcon">
        <span class="msg-point" style=""></span>
      </div>
      <div>
        <a-drawer
            title="催命消息中心"
            placement="right"
            :closable="true"
            :maskClosable="true"
            :visible="msgVisible"
            @close="onClose"
        >
          <a-spin :spinning="loading" style="min-height: 200px;">
            <div class="list-content">
              <div class="notification-view">
                <div class="list">
                  <div class="notification-item flex-view" v-for="item in msgData">
                    <!---->
                    <div class="content-box">
                      <div class="header">
                        <span class="title-txt">{{item.title}}</span>
                        <br/>
                        <span class="time">{{ item.create_time }}</span>
                      </div>
                      <div class="head-text">
                      </div>
                      <div class="content">
                        <p>{{ item.content }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </a-spin>
        </a-drawer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {listApi} from '/@/api/index/notice'
import {useUserStore} from "/@/store";
const logoImage = '/images/cattlehores.png';
import SearchIcon from '/@/assets/images/search-icon.svg';
import AvatarIcon from '/@/assets/images/avatar.jpg';
import MessageIcon from '/@/assets/images/message-icon.svg';

import {message} from "ant-design-vue";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const keywordRef = ref()

let loading = ref(false)
let msgVisible = ref(false)
let msgData = ref([] as any)

onMounted(()=>{
  getMessageList()
})

const getMessageList = ()=> {
  loading.value = true
  listApi({}).then(res => {
    msgData.value = res.data
    loading.value = false
  }).catch(err => {
    console.log(err)
    loading.value = false
  })
}
const search = () => {
  const keyword = keywordRef.value.value
  if (route.name === 'search') {
    router.push({name: 'search', query: {keyword: keyword}})
  } else {
    let text = router.resolve({name: 'search', query: {keyword: keyword}})
    window.open(text.href, '_blank')
  }
}
const goLogin = () => {
  router.push({name: 'login'})
}

const handleZhaoren = () => {
  let userId = userStore.user_id
  if(userId){
    router.push({name: 'myThingView'})
  }else {
    message.warn('想压榨牛马？请先登录')
  }

}

const goUserCenter = (menuName) => {
  router.push({name: menuName})
}
const quit= () => {
  userStore.logout().then(res => {
    router.push({name: 'portal'})
  })
}
const onClose = () => {
  msgVisible.value = false;
}

</script>

<style scoped lang="less">
.main-bar-view {
  position: fixed;
  top: 0;
  left: 0;
  height: 56px;
  width: 100%;
  background: var(--nm-dark);
  border-bottom: 3px solid var(--nm-primary);
  padding-left: 48px;
  z-index: 16;
  display: flex;
  flex-direction: row;
  align-items: center;
  box-shadow: 0 2px 16px rgba(0,0,0,0.4);
}

.logo {
  margin-right: 28px;
  img {
    height: 36px;
    width: auto;
    cursor: pointer;
    filter: none;
    transition: transform 0.2s, opacity 0.2s;
    &:hover {
      transform: scale(1.05);
      opacity: 0.9;
    }
  }
}

.search-entry {
  position: relative;
  width: 380px;
  min-width: 200px;
  height: 34px;
  background: var(--nm-dark-2);
  border: 1px solid var(--nm-dark-3);
  padding: 0 12px;
  border-radius: var(--nm-radius-sm);
  font-size: 0;
  cursor: pointer;
  transition: border-color 0.2s;

  &:focus-within {
    border-color: var(--nm-primary);
  }

  img {
    max-width: 100%;
    height: auto;
    filter: brightness(0.6);
  }
  .search-icon {
    width: 16px;
    margin: 9px 8px 0 0;
  }
  input {
    position: absolute;
    top: 5px;
    width: 82%;
    height: 24px;
    border: none;
    outline: none;
    color: #e7e5e4;
    background: transparent;
    font-size: 13px;
    letter-spacing: 0.3px;

    &::placeholder {
      color: #78716c;
    }
  }
}

.right-view {
  padding-right: 36px;
  flex: 1;
  display: flex;
  flex-direction: row;
  gap: 20px;
  justify-content: flex-end;
  align-items: center;

  a {
    color: #d6d3d1 !important;
    transition: color 0.2s;
    &:hover {
      color: var(--nm-primary) !important;
    }
  }

  button {
    outline: none;
    border: none;
    cursor: pointer;
  }
  img {
    cursor: pointer;
  }
  .right-icon {
    position: relative;
    width: 22px;
    margin: 4px 0 0 4px;
    cursor: pointer;
    display: inline-block;
    font-size: 0;
    img {
      filter: brightness(0.7) invert(1);
    }
    &:hover img {
      filter: brightness(1) invert(1) sepia(1) saturate(5) hue-rotate(330deg);
    }
    span {
      position: absolute;
      right: -15px;
      top: -3px;
      font-size: 12px;
      color: #fff;
      background: var(--nm-primary);
      border-radius: 8px;
      padding: 0 4px;
      height: 16px;
      line-height: 16px;
      font-weight: 600;
      min-width: 20px;
      text-align: center;
    }
    .msg-point {
      position: absolute;
      right: -4px;
      top: 0;
      min-width: 8px;
      width: 8px;
      height: 8px;
      background: var(--nm-primary);
      border-radius: 50%;
    }
  }

  .self-img {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    vertical-align: middle;
    cursor: pointer;
    border: 2px solid var(--nm-dark-3);
    transition: border-color 0.2s;
    &:hover {
      border-color: var(--nm-primary);
    }
  }
  .btn {
    background: var(--nm-primary);
    font-size: 13px;
    font-weight: 600;
    color: #fff;
    border-radius: var(--nm-radius-sm);
    text-align: center;
    padding: 0 16px;
    height: 32px;
    line-height: 32px;
    vertical-align: middle;
    margin-left: 16px;
    letter-spacing: 0.5px;
    transition: background 0.2s, transform 0.1s;
    &:hover {
      background: var(--nm-primary-hover);
      transform: translateY(-1px);
    }
    &:active {
      transform: translateY(0);
    }
  }
}

.content-list {
  flex: 1;

  .list-title {
    color: var(--nm-text-main);
    font-weight: 700;
    font-size: 16px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 2px solid var(--nm-primary);
    padding-bottom: 8px;
  }
}

.notification-item {
  padding-top: 16px;

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 8px;
  }

  .content-box {
    flex: 1;
    border-bottom: 1px dashed var(--nm-border);
    padding: 4px 0 16px;
  }

  .header {
    margin-bottom: 12px;
  }

  .title-txt {
    color: var(--nm-primary);
    font-weight: 600;
    font-size: 14px;
  }

  .time {
    color: var(--nm-text-muted);
    font-size: 13px;
  }

  .head-text {
    color: var(--nm-text-main);
    font-weight: 500;
    font-size: 14px;
    line-height: 22px;

    .name {
      margin-right: 8px;
    }
  }

  .content {
    margin-top: 4px;
    color: var(--nm-text-sub);
    font-size: 14px;
    line-height: 22px;
  }
}
</style>
