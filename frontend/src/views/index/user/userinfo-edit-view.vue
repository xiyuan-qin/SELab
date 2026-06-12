<template>
  <div class="content-list">
    <div class="list-title">设置</div>
    <a-spin :spinning="loading" style="min-height: 200px;">
      <div class="list-content">
      <div class="edit-view">
        <div class="item flex-view">
          <div class="label">头像</div>
          <div class="right-box avatar-box flex-view">
            <img v-if="tData.form && tData.form.avatar" :src="tData.form.avatar" class="avatar">
            <img v-else :src="AvatarIcon" class="avatar">
            <div class="change-tips flex-view">
                <a-upload
                  name="file"
                  accept="image/*"
                  :multiple="false"
                  :before-upload="beforeUpload"
                >
                  <label>点击更换头像</label>
                </a-upload>
              <p class="tip">图片格式支持 GIF、PNG、JPEG，尺寸不小于 200 PX，小于 4 MB</p>
            </div>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">昵称</div>
          <div class="right-box">
            <input type="text" v-model="tData.form.nickname" placeholder="请输入昵称" maxlength="20" class="input-dom">
            <p class="tip">支持中英文，长度不能超过 20 个字符</p>
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">手机号</div>
          <div class="right-box">
            <input type="text" v-model="tData.form.mobile" placeholder="请输入邮箱" maxlength="100" class="input-dom web-input">
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">邮箱</div>
          <div class="right-box">
            <input type="text" v-model="tData.form.email" placeholder="请输入邮箱" maxlength="100" class="input-dom web-input">
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">个人简介</div>
          <div class="right-box">
          <textarea v-model="tData.form.description" placeholder="请输入简介" maxlength="200" class="intro">
          </textarea>
            <p class="tip">限制200字以内</p>
          </div>
        </div>
        <button class="save mg" @click="submit()">保存</button>
      </div>
    </div>
    </a-spin>
  </div>
</template>

<script setup>
import {message} from "ant-design-vue";
import {detailApi, updateUserInfoApi} from '/@/api/index/user'
import {BASE_URL} from "/@/store/constants";
import {useUserStore} from "/@/store";
import AvatarIcon from '/@/assets/images/avatar.jpg'

const router = useRouter();
const userStore = useUserStore();

let loading = ref(false)
let tData = reactive({
  form:{
    avatar: undefined,
    avatarFile: undefined,
    nickname: undefined,
    email: undefined,
    mobile: undefined,
    description: undefined,
  }
})

onMounted(()=>{
  getUserInfo()
})

const beforeUpload =(file)=> {
  // 改文件名
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
  const copyFile = new File([file], fileName)
  console.log(copyFile)
  tData.form.avatarFile = copyFile
  return false
}

const getUserInfo =()=> {
  loading.value = true
  let userId = userStore.user_id
  detailApi({id: userId}).then(res => {
    tData.form = res.data
    if (tData.form.avatar) {
      tData.form.avatar = BASE_URL  + tData.form.avatar
    }
    loading.value = false
  }).catch(err => {
    console.log(err)
    loading.value = false
  })
}
const submit =()=> {
  let formData = new FormData()
  let userId = userStore.user_id
  if (tData.form.avatarFile) {
    formData.append('avatar', tData.form.avatarFile)
  }
  if (tData.form.nickname) {
    formData.append('nickname', tData.form.nickname)
  }
  if (tData.form.email) {
    formData.append('email', tData.form.email)
  }
  if (tData.form.mobile) {
    formData.append('mobile', tData.form.mobile)
  }
  if (tData.form.description) {
    formData.append('description', tData.form.description)
  }
  updateUserInfoApi({
    id: userId
  },formData).then(res => {
    message.success('保存成功')
    getUserInfo()
  }).catch(err => {
    console.log(err)
  })
}

</script>

<style scoped lang="less">
input, textarea {
  border-style: none;
  outline: none;
  margin: 0;
  padding: 0;
}

.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  flex: 1;

  .list-title {
    color: var(--nm-text-main);
    font-weight: 700;
    font-size: var(--nm-fs-lg);
    line-height: 40px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--nm-border);
  }

  .edit-view {
    .item {
      display: flex;
      align-items: flex-start;
      margin: 22px 0;

      .label {
        width: 96px;
        padding-top: 10px;
        color: var(--nm-text-sub);
        font-weight: 600;
        font-size: var(--nm-fs-base);
        flex-shrink: 0;
      }

      .right-box {
        flex: 1;
      }

      .avatar {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        margin-right: 16px;
        border: 2px solid var(--nm-border);
      }

      .change-tips {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
      }

      label {
        color: var(--nm-primary);
        font-size: var(--nm-fs-base);
        line-height: 22px;
        cursor: pointer;
        display: block;
        font-weight: 600;
      }

      .input-dom {
        width: 400px;
        max-width: 100%;
        background: var(--nm-bg-soft);
        border: 1px solid var(--nm-border);
        border-radius: var(--nm-radius);
        height: 40px;
        line-height: 40px;
        font-size: var(--nm-fs-base);
        color: var(--nm-text-main);
        padding: 0 12px;
        transition: border-color 0.2s;
        &:focus { border-color: var(--nm-primary); background: #fff; }
      }

      .tip {
        font-size: var(--nm-fs-xs);
        line-height: 16px;
        color: var(--nm-text-muted);
        margin-top: 6px;
      }

      .intro {
        resize: none;
        background: var(--nm-bg-soft);
        border: 1px solid var(--nm-border);
        border-radius: var(--nm-radius);
        width: 100%;
        padding: 8px 12px;
        height: 90px;
        line-height: 22px;
        font-size: var(--nm-fs-base);
        color: var(--nm-text-main);
        transition: border-color 0.2s;
        &:focus { border-color: var(--nm-primary); background: #fff; }
      }
    }

    .save {
      background: var(--nm-primary);
      border-radius: var(--nm-radius);
      width: 110px;
      height: 40px;
      line-height: 40px;
      font-size: var(--nm-fs-base);
      font-weight: 600;
      color: #fff;
      border: none;
      outline: none;
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
      &:hover { background: var(--nm-primary-hover); transform: translateY(-1px); }
    }

    .mg {
      margin-left: 96px;
    }
  }
}

</style>
