<template>
  <div class="footer-view">
    <div class="foot-link-box flex-view">
      <a href="https://github.com/geeeeeeeek/java_shop" class="foot-link" target="_blank">平台说明</a>
      <div class="link-split"></div>
      <a href="/#/admin" class="foot-link" target="_blank">管理后台</a>
      <div class="link-split"></div>
      <a href="" class="foot-link" target="_blank">关于牛马直聘</a>
    </div>
    <div class="footer-infos">
      <span>
        <a style="color: rgb(174, 174, 174);">牛马直聘 · 平台备案信息</a>
      </span>
      <span>&nbsp;&nbsp;专注招聘求职双向匹配&nbsp;&nbsp;让机会和人才高效连接</span>
    </div>
    <div class="address">2022-2026 © 牛马直聘 · All Rights Reserved</div>
  </div>
</template>

<script>
export default {
  name: 'Footer',
  data () {
    return {}
  },
  methods: {}
}
</script>

<style scoped lang="less">
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.footer-view {
  max-width: 1108px;
  margin: 0 auto;
  padding: 24px 0 20px 54px;

  .foot-link-box {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    overflow: hidden;
    margin: 24px auto 16px;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    .foot-link {
      margin: 0 16px;
      color: var(--nm-primary);
    }
    a {
      background-color: transparent;
      text-decoration: none;
      color: var(--nm-primary);
    }
  }

  .footer-infos {
    height: 16px;
    line-height: 16px;
    font-size: 12px;
    padding-left: 63px;
    color: #aeaeae;
    margin-top: 16px;
    text-align: center;
  }
  .address {
    text-align: center;
    height: 16px;
    line-height: 16px;
    font-size: 12px;
    color: #aeaeae;
    margin-top: 8px;
  }
}
</style>
