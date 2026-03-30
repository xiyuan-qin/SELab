<template>
  <div class="content">
    <div class="content-left">
      <div class="left-search-item">
        <h4>坑的种类</h4>
        <a-tree :tree-data="contentData.cData" :selected-keys="contentData.selectedKeys" @select="onSelect"
                style="min-height: 220px;">
        </a-tree>
      </div>
      <div class="left-search-item"><h4>热门坑位</h4>
        <div class="tag-view tag-flex-view">
            <span class="tag" :class="{'tag-select': contentData.selectTagId===item.id}"
                  v-for="item in contentData.tagData" :key="item.id"
                  @click="clickTag(item.id)">{{ item.title }}</span>
        </div>
      </div>
    </div>
    <div class="content-right">
      <div class="top-select-view flex-view">
        <div class="order-view">
          <span class="title"></span>
          <span class="tab"
                :class="contentData.selectTabIndex===index? 'tab-select':''"
                v-for="(item,index) in contentData.tabData"
                :key="index"
                @click="selectTab(index)">
            {{ item }}
          </span>
          <span :style="{left: contentData.tabUnderLeft + 'px'}" class="tab-underline"></span>
        </div>
      </div>
      <a-spin :spinning="contentData.loading" style="min-height: 200px;">
        <div class="pc-thing-list flex-view">
          <div class="sub-li" v-for="item in contentData.pageData" @click="handleDetail(item)">
            <a class="job-info" target="_blank">
              <div class="sub-li-top">
                <div class="sub-li-info">
                  <p class="name">{{item.title}}</p>
                </div>
                <p class="salary">{{item.salary}}</p>
              </div>
              <p class="job-text">
                <span>{{item.location}}</span>
                <span>{{item.work_expe}}</span>
                <span>{{item.education}}</span>
              </p>
            </a>
          </div>
          <div v-if="contentData.pageData.length <= 0 && !contentData.loading" class="no-data" style="">今日坑位已满，请明日再来</div>
        </div>
      </a-spin>
      <div class="page-view" style="">
        <a-pagination v-model="contentData.page" size="small" @change="changePage" :hideOnSinglePage="true"
                      :defaultPageSize="contentData.pageSize" :total="contentData.total" :showSizeChanger="false"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import {listApi as listClassificationList} from '/@/api/index/classification'
import {listApi as listTagList} from '/@/api/index/tag'
import {listApi as listThingList} from '/@/api/index/thing'
import {BASE_URL} from "/@/store/constants";
import {useUserStore} from "/@/store";

const userStore = useUserStore()
const router = useRouter();

const contentData = reactive({
  selectX: 0,
  selectTagId: -1,
  cData: [],
  selectedKeys: [],
  tagData: [],
  loading: false,

  tabData: ['最新的坑', '最烫的坑', '为你推坑'],
  selectTabIndex: 0,
  tabUnderLeft: 12,

  thingData: [],
  pageData: [],

  page: 1,
  total: 0,
  pageSize: 15,
})

onMounted(() => {
  initSider()
  getThingList({})
})

const initSider = () => {
  contentData.cData.push({key:'-1', title:'全部'})
  listClassificationList().then(res => {
    res.data.forEach(item=>{
      item.key = item.id
      contentData.cData.push(item)
    })
  })
  listTagList().then(res => {
    contentData.tagData = res.data
  })
}

const getSelectedKey = () => {
  if (contentData.selectedKeys.length > 0) {
    return contentData.selectedKeys[0]
  } else {
    return -1
  }
}
const onSelect = (selectedKeys) => {
  contentData.selectedKeys = selectedKeys
  console.log(contentData.selectedKeys[0])
  if (contentData.selectedKeys.length > 0) {
    getThingList({c: getSelectedKey()})
  }
  contentData.selectTagId = -1
}
const clickTag = (index) => {
  contentData.selectedKeys = []
  contentData.selectTagId = index
  getThingList({tag: contentData.selectTagId})
}

// 最新|最热|推荐
const selectTab = (index) => {
  contentData.selectTabIndex = index
  contentData.tabUnderLeft = 12 + 50 * index
  console.log(contentData.selectTabIndex)
  let sort = (index === 0 ? 'recent' : index === 1 ? 'hot' : 'recommend')
  const data = {sort: sort}
  if (contentData.selectTagId !== -1) {
    data['tag'] = contentData.selectTagId
  } else {
    data['c'] = getSelectedKey()
  }
  getThingList(data)
}
const handleDetail = (item) => {
  // 跳转新页面
  let text = router.resolve({name: 'detail', query: {id: item.id}})
  window.open(text.href, '_blank')
}
// 分页事件
const changePage = (page) => {
  contentData.page = page
  let start = (contentData.page - 1) * contentData.pageSize
  contentData.pageData = contentData.thingData.slice(start, start + contentData.pageSize)
  console.log('第' + contentData.page + '页')
}
const getThingList = (data) => {
  contentData.loading = true
  listThingList(data).then(res => {
    contentData.loading = false
    res.data.forEach((item, index) => {
      if (item.cover) {
        item.cover = BASE_URL +  item.cover
      }
    })
    console.log(res)
    contentData.thingData = res.data
    contentData.total = contentData.thingData.length
    changePage(1)
  }).catch(err => {
    console.log(err)
    contentData.loading = false
  })
}


</script>

<style scoped lang="less">
.content {
  display: flex;
  flex-direction: row;
  width: 1100px;
  margin: 32px auto 80px;
}

.content-left {
  width: 220px;
  margin-right: 32px;
}

.left-search-item {
  overflow: hidden;
  border-bottom: 1px solid var(--nm-border);
  margin-top: 24px;
  padding-bottom: 24px;
}

h4 {
  color: var(--nm-text-main);
  font-weight: 700;
  font-size: 14px;
  line-height: 22px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding-left: 8px;
  border-left: 3px solid var(--nm-primary);
}

.category-item {
  cursor: pointer;
  color: #333;
  margin: 12px 0 0;
  padding-left: 16px;
}

ul {
  margin: 0;
  padding: 0;
}

ul {
  list-style-type: none;
}

li {
  margin: 4px 0 0;
  display: list-item;
  text-align: -webkit-match-parent;
}

.child {
  color: #333;
  padding-left: 16px;
}

.child:hover {
  color: #4684e2;
}

.select {
  color: #4684e2;
}

.flex-view {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  //justify-content: space-between;
  display: flex;
}

.name {
  font-size: 14px;
}

.name:hover {
  color: #4684e2;
}

.count {
  font-size: 14px;
  color: #999;
}

.check-item {
  font-size: 0;
  height: 18px;
  line-height: 12px;
  margin: 12px 0 0;
  color: #333;
  cursor: pointer;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

.check-item input {
  cursor: pointer;
}

.check-item label {
  font-size: 14px;
  margin-left: 12px;
  cursor: pointer;
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
}

.tag-view {
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  margin-top: 4px;
}

.tag-flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.tag {
  background: var(--nm-bg-soft);
  border: 1px solid var(--nm-border);
  box-sizing: border-box;
  border-radius: var(--nm-radius-sm);
  height: 22px;
  line-height: 20px;
  padding: 0 10px;
  margin: 8px 6px 0 0;
  cursor: pointer;
  font-size: 12px;
  color: var(--nm-text-sub);
  transition: all 0.15s;
}

.tag:hover {
  background: var(--nm-primary);
  color: #fff;
  border-color: var(--nm-primary);
}

.tag-select {
  background: var(--nm-primary);
  color: #fff;
  border-color: var(--nm-primary);
  font-weight: 600;
}

.content-right {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  padding-top: 12px;

  .pc-search-view {
    margin: 0 0 24px;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;

    .search-icon {
      width: 20px;
      height: 20px;
      -webkit-box-flex: 0;
      -ms-flex: 0 0 20px;
      flex: 0 0 20px;
      margin-right: 16px;
    }

    input {
      outline: none;
      border: 0px;
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      border-bottom: 1px solid #cedce4;
      color: #152844;
      font-size: 14px;
      height: 22px;
      line-height: 22px;
      -ms-flex-item-align: end;
      align-self: flex-end;
      padding-bottom: 8px;
    }

    .clear-search-icon {
      position: relative;
      left: -20px;
      cursor: pointer;
    }

    button {
      outline: none;
      border: none;
      font-size: 14px;
      color: #fff;
      background: #288dda;
      border-radius: 32px;
      width: 88px;
      height: 32px;
      line-height: 32px;
      margin-left: 2px;
      cursor: pointer;
    }

    .float-count {
      color: #999;
      margin-left: 24px;
    }
  }

  .flex-view {
    display: flex;
  }

  .top-select-view {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    height: 40px;
    line-height: 40px;

    .type-view {
      position: relative;
      font-weight: 400;
      font-size: 18px;
      color: #5f77a6;

      .type-tab {
        margin-right: 32px;
        cursor: pointer;
      }

      .type-tab-select {
        color: #152844;
        font-weight: 600;
        font-size: 20px;
      }

      .tab-underline {
        position: absolute;
        bottom: 0;
        //left: 22px;
        width: 16px;
        height: 4px;
        background: var(--nm-accent);
        -webkit-transition: left .3s;
        transition: left .3s;
      }
    }

    .order-view {
      position: relative;
      color: var(--nm-text-sub);
      font-size: 13px;

      .title {
        margin-right: 8px;
      }

      .tab {
        color: var(--nm-text-muted);
        margin-right: 4px;
        cursor: pointer;
        padding: 4px 12px;
        border-radius: var(--nm-radius-sm);
        transition: all 0.15s;
        display: inline-block;

        &:hover {
          color: var(--nm-primary);
          background: rgba(234,88,12,0.06);
        }
      }

      .tab-select {
        color: var(--nm-primary);
        font-weight: 700;
        background: rgba(234,88,12,0.08);
      }

      .tab-underline {
        display: none;
      }
    }

  }

  .pc-thing-list {
    margin-top: 24px;
    flex-wrap: wrap;
    gap: 16px;

    .sub-li {
      background: var(--nm-bg-card);
      height: 120px;
      overflow: hidden;
      transition: all 0.2s ease;
      display: block;
      width: 260px;
      font-size: 0;
      padding: 0;
      box-sizing: border-box;
      border: 1px solid var(--nm-border);
      border-left: 3px solid var(--nm-border);
      border-radius: var(--nm-radius);
      cursor: pointer;
      position: relative;

      &:hover {
        border-left-color: var(--nm-primary);
        box-shadow: var(--nm-shadow-md);
        transform: translateY(-2px);
      }

      .job-info {
        padding: 16px 18px;
        box-sizing: border-box;
        display: block;
      }
      .sub-li-top {
        margin-bottom: 10px;
        display: flex;
        width: 100%;
        align-items: center;
        justify-content: space-between;
        .name {
          color: var(--nm-text-main);
          font-size: 15px;
          font-weight: 600;
          line-height: 22px;
          transition: color 0.2s;
          position: relative;
          max-width: 160px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .salary {
          font-size: 15px;
          font-weight: 700;
          color: var(--nm-primary);
          line-height: 22px;
          flex: none;
          letter-spacing: -0.3px;
        }
      }
      &:hover .name {
        color: var(--nm-primary);
      }
      .sub-li-info {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        height: 22px;
        overflow: hidden;
        flex: 1;
      }
      .job-text {
        white-space: normal;
        height: 22px;
        line-height: 22px;
        overflow: hidden;
        word-break: break-all;
        display: flex;
        gap: 6px;
        span {
          display: inline-block;
          height: 20px;
          font-size: 12px;
          font-weight: 400;
          color: var(--nm-text-sub);
          line-height: 20px;
          padding: 0 8px;
          border-radius: 2px;
          background: var(--nm-bg-soft);
          border: 1px solid var(--nm-border);
        }
      }
    }


    .no-data {
      height: 200px;
      line-height: 200px;
      text-align: center;
      width: 100%;
      font-size: 16px;
      color: var(--nm-text-sub);
    }
  }

  .page-view {
    width: 100%;
    text-align: center;
    margin-top: 48px;
  }
}

.a-price-symbol {
  top: -0.5em;
  font-size: 12px;
}

.a-price {
  color: #0F1111;
  font-size: 21px;
}

</style>
