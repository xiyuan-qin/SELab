<template>
  <a-config-provider :locale="zhCN">
    <router-view />
  </a-config-provider>
</template>
<script setup lang="ts">

import zhCN from 'ant-design-vue/es/locale/zh_CN';

</script>

<style>

  #app {
    font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
    min-height: 100vh;
    color: var(--nm-text-main);
    background: #fff;
  }
</style>
