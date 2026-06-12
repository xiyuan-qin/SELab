<template>
  <div class="content-list">
    <div class="list-title">投递管理</div>
    <a-spin :spinning="loading" style="min-height: 200px;">
      <div class="list-content">
      <div class="order-item-view" v-for="(item, index) in postData" :key="index">
        <div class="header flex-view">
          <div class="left">
            <span class="text">投递编号</span>
            <span class="num mg-4">#</span>
            <span class="num">{{item.id}}</span>
          </div>
          <div class="right">
            <span class="text">投递状态</span>
            <span class="state">正常</span>
          </div>
        </div>
        <div class="bottom flex-view">
          <div class="left">
            <span class="text">{{item.thing_title}}</span>
          </div>
          <div class="right flex-view">
            <span class="text">投递人</span>
            <span class="num">{{item.user_username}}</span>
            <span class="open" @click="handleResume(item)">简历</span>
            <span class="text">投递时间</span>
            <span class="money">{{item.create_time}}</span>
          </div>
        </div>
      </div>
      <template v-if="!postData || postData.length <= 0">
        <a-empty style="width: 100%;margin-top: 200px;"/>
      </template>
    </div>
    </a-spin>
  </div>
</template>

<script setup>
import {message} from "ant-design-vue";
import {listCompanyPostApi} from '/@/api/index/post'
import {listUserCompanyApi} from '/@/api/index/company'
import {BASE_URL} from "/@/store/constants";
import {useUserStore} from "/@/store";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const loading = ref(false)
const postData = ref([])
const orderStatus = ref('')

onMounted(()=>{
  getList()
})


const getList= ()=> {
  loading.value = true

  let userId = userStore.user_id

  listUserCompanyApi({userId: userId}).then(res=>{
    if(res.data && res.data.length>0){
      let company = res.data[0]
      listCompanyPostApi({companyId: company.id}).then(res => {
        postData.value = res.data
        loading.value = false
      }).catch(err => {
        console.log(err)
        loading.value = false
      })
    }else {
      message.warn("请完善公司资料")
      loading.value = false
    }
  }).catch(err=>{

  })


}
const handleResume =(item) =>{
  // 跳转新页面
  message.warn("功能开发中")
}


</script>
<style scoped lang="less">
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;

  .list-title {
    color: var(--nm-text-main);
    font-weight: 600;
    font-size: 18px;
    line-height: 24px;
    height: 24px;
    margin-bottom: 4px;
  }
}

.order-item-view {
  background: #f7f9fb;
  border-radius: 4px;
  padding: 16px;
  margin-top: 12px;

  .header {
    border-bottom: 1px solid var(--nm-border);
    padding-bottom: 12px;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;

    .text {
      color: var(--nm-text-sub);
    }

    .mg-4 {
      margin-left: 4px;
    }

    .num {
      font-weight: 500;
      color: var(--nm-text-main);
    }

    .num {
      font-weight: 500;
      color: var(--nm-text-main);
    }

    .time {
      margin-left: 16px;
      color: #a1adc5;
    }

    .state {
      color: #ff7b31;
      font-weight: 600;
      margin-left: 10px;
    }
  }

  .content {
    padding: 12px 0;
    overflow: hidden;

    .left-list {
      overflow: hidden;
      height: 132px;
      -webkit-box-flex: 2;
      -ms-flex: 2;
      flex: 2;
      padding-right: 16px;

      .list-item {
        height: 60px;
        margin-bottom: 12px;
        overflow: hidden;
        cursor: pointer;
      }

      .thing-img {
        width: 48px;
        height: 100%;
        margin-right: 12px;
      }

      .detail {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-top {
        -webkit-box-align: start;
        -ms-flex-align: start;
        align-items: flex-start;
      }

      .name {
        color: var(--nm-text-main);
        font-weight: 600;
        font-size: 14px;
        line-height: 18px;
      }

      .count {
        color: #484848;
        font-size: 12px;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-center {
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
      }

      .type {
        color: var(--nm-text-sub);
        font-size: 12px;
      }

      .price {
        color: #ff7b31;
        font-weight: 600;
        font-size: 14px;
      }
    }

    .right-info {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      border-left: 1px solid var(--nm-border);
      padding-left: 12px;
      line-height: 22px;
      font-size: 14px;

      .title {
        color: var(--nm-text-sub);
      }

      .name {
        color: var(--nm-text-main);
      }

      .text {
        color: #484848;
      }

      .mg {
        margin-bottom: 4px;
      }
    }
  }

  .bottom {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;
    padding-top: 14px;

    .text {
      color: var(--nm-text-sub);
    }

    .open {
      margin-right: 16px;
      color: var(--nm-primary);
      cursor: pointer;
    }

    .right {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
    }

    .text {
      color: var(--nm-text-sub);
    }

    .num {
      color: var(--nm-text-main);
      margin: 0 8px 0 8px;
    }

    .money {
      font-size: 14px;
      color: var(--nm-text-sub);
      margin-left: 8px;
    }
  }

}

.order-item-view:first-child {
  margin-top: 16px;
}

</style>
