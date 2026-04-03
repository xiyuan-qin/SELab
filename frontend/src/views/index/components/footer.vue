<template>
  <div class="footer-shell">
    <div class="footer-view">
      <div class="foot-link-box flex-view">
        <a href="https://github.com/geeeeeeeek/java_shop" class="foot-link" target="_blank">牛马须知</a>
        <a href="/#/admin" class="foot-link" target="_blank">老板后台</a>
        <a href="" class="foot-link" target="_blank">关于这个坑</a>
      </div>
      <div class="footer-infos">
        <span>牛马直聘 · 劳动局已备案（但没用）</span>
        <span>&nbsp;&nbsp;专注牛马与老板的精准配对&nbsp;&nbsp;让剥削与被剥削高效对接</span>
      </div>
      <div class="address">2022-2026 © 牛马直聘 · 牛马永不为奴（但还是得上班）</div>
    </div>
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
  display: flex;
}

.footer-shell {
  width: 100%;
  background: var(--nm-dark);
  border-top: 3px solid var(--nm-primary);
}

.footer-view {
  max-width: 1108px;
  margin: 0 auto;
  padding: 32px 0 24px;

  .foot-link-box {
    display: flex;
    align-items: center;
    overflow: hidden;
    margin: 0 auto 20px;
    justify-content: center;
    gap: 8px;

    .link-split {
      display: none;
    }

    .foot-link,
    a {
      color: #a8a29e !important;
      text-decoration: none;
      font-size: 13px;
      padding: 4px 16px;
      border: 1px solid var(--nm-dark-3);
      border-radius: var(--nm-radius-sm);
      transition: all 0.2s;

      &:hover {
        color: var(--nm-primary) !important;
        border-color: var(--nm-primary);
        background: rgba(234, 88, 12, 0.08);
      }
    }
  }

  .footer-infos {
    line-height: 20px;
    font-size: 12px;
    color: #57534e;
    margin-top: 0;
    text-align: center;
    padding: 0;

    a {
      color: #44403c !important;
    }

    span {
      color: #57534e;
    }
  }

  .address {
    text-align: center;
    line-height: 20px;
    font-size: 12px;
    color: #44403c;
    margin-top: 8px;
  }
}
</style>
